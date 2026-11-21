-- Run after the command center migration on a disposable Supabase database.
begin;

-- The web server can invoke the command RPCs. Application clients cannot.
do $$
begin
  if has_function_privilege('anon', 'public.cm_command_state(uuid)', 'EXECUTE')
    or has_function_privilege('authenticated', 'public.cm_command_mutate(uuid,jsonb)', 'EXECUTE')
    or has_function_privilege('authenticated', 'public.cm_command_begin_agent(uuid,jsonb)', 'EXECUTE')
    or has_function_privilege('anon', 'public.cm_command_tick(uuid)', 'EXECUTE')
    or has_schema_privilege('authenticated', 'cm_command', 'USAGE') then
    raise exception 'Application clients can access workspace storage directly';
  end if;
  if has_table_privilege('service_role', 'cm_command.audit', 'UPDATE,DELETE') then
    raise exception 'Audit rows can be changed by the service role';
  end if;
end;
$$;

set local role service_role;
do $$
declare
  owner_a uuid := gen_random_uuid();
  owner_b uuid := gen_random_uuid();
  state jsonb;
  source_id uuid;
  approval_id uuid;
  request jsonb;
  lease uuid;
  run_id uuid;
  result jsonb;
begin
  state := public.cm_command_state(owner_a);
  if jsonb_array_length(state->'automations') <> 6 or exists (select from jsonb_array_elements(state->'automations') item where not (item->>'paused')::boolean) then
    raise exception 'New workspace automation defaults are incorrect';
  end if;
  begin
    perform public.cm_command_mutate(owner_a, '{"kind":"save_record","area":"nation","title":"TestFlight","stage":"Resolved"}');
    raise exception 'Evidence requirement did not reject a release record';
  exception when sqlstate 'CM004' then null;
  end;
  state := public.cm_command_mutate(owner_a, '{"kind":"save_record","area":"library","title":"Test theme","stage":"Approved theme","body":"Build through pressure"}');
  source_id := (state #>> '{records,0,id}')::uuid;
  if jsonb_array_length(public.cm_command_state(owner_b)->'records') <> 0 then
    raise exception 'One owner can inspect another owner’s records';
  end if;
  request := jsonb_build_object('kind','request_approval','action','external_communication','title','Review this message','body','Exact proposal','record_id',source_id,'dedupe_key','same');
  begin
    perform public.cm_command_mutate(owner_b, request);
    raise exception 'Cross-owner approval attachment was accepted';
  exception when sqlstate 'CM002' then null;
  end;
  perform public.cm_command_mutate(owner_a, request);
  state := public.cm_command_mutate(owner_a, request);
  approval_id := (state #>> '{approvals,0,id}')::uuid;
  if jsonb_array_length(state->'approvals') <> 1 or state #>> '{approvals,0,status}' <> 'pending' then
    raise exception 'Approval deduplication failed';
  end if;
  begin
    perform public.cm_command_mutate(owner_a, request || '{"body":"Different proposal"}');
    raise exception 'Different proposal reused an approval identifier';
  exception when sqlstate 'CM003' then null;
  end;
  request := jsonb_build_object('kind','decide_approval','id',approval_id,'decision','approved','note','Test only');
  begin
    perform public.cm_command_mutate(owner_b, request);
    raise exception 'Cross-owner approval decision was accepted';
  exception when sqlstate 'CM002' then null;
  end;
  perform public.cm_command_mutate(owner_a, request);
  state := public.cm_command_mutate(owner_a, request);
  if state #>> '{approvals,0,status}' <> 'approved' or
     (select count(*) from jsonb_array_elements(state->'audit') item where item->>'event' = 'approval.decided') <> 1 then
    raise exception 'Approval decision or immutable audit result is incorrect';
  end if;
  begin
    perform public.cm_command_mutate(owner_a, request || '{"decision":"rejected"}');
    raise exception 'An already decided approval changed';
  exception when sqlstate 'CM003' then null;
  end;
  request := jsonb_build_object('kind','run_automation','key','content-draft','event_key','first','trigger',jsonb_build_object('record_id',source_id));
  begin
    perform public.cm_command_mutate(owner_a, request);
    raise exception 'Paused automation accepted a run';
  exception when sqlstate 'CM005' then null;
  end;
  perform public.cm_command_mutate(owner_a, '{"kind":"set_automation","key":"content-draft","paused":false,"interval_minutes":60}');
  perform public.cm_command_mutate(owner_a, request);
  state := public.cm_command_mutate(owner_a, request || '{"event_key":"second"}');
  if jsonb_array_length(state->'runs') <> 1 or state #>> '{runs,0,status}' <> 'succeeded' or
     (select count(*) from jsonb_array_elements(state->'records') item where item->>'title' = 'Draft package · Test theme') <> 1 then
    raise exception 'Content source produced duplicate artifacts or no successful run';
  end if;
  perform public.cm_command_mutate(owner_a, '{"kind":"set_automation","key":"daily-briefing","paused":false,"interval_minutes":1440}');
  update cm_command.automations set next_run_at = now() - interval '1 minute' where owner_id = owner_a and key = 'daily-briefing';
  if public.cm_command_tick(owner_a)->>'processed' <> '1' or public.cm_command_tick(owner_a)->>'processed' <> '0' then
    raise exception 'Scheduled briefing did not run once when due';
  end if;
  state := public.cm_command_state(owner_a);
  if not exists (select from jsonb_array_elements(state->'records') item where item->>'area' = 'executive' and item->>'body' like '%Pending owner decisions: 0%') then
    raise exception 'Scheduled briefing did not create an evidence-scoped draft';
  end if;

  request := '{"dedupe_key":"agent-first","agent":"ceo","brief":"Summarize my priorities"}';
  result := public.cm_command_begin_agent(owner_a, request);
  lease := (result->>'lease')::uuid;
  run_id := (result #>> '{run,id}')::uuid;
  if result->>'claimed' <> 'true' or lease is null then raise exception 'Agent claim did not acquire a lease'; end if;
  result := public.cm_command_begin_agent(owner_a, request);
  if result->>'claimed' <> 'false' or result ? 'lease' then raise exception 'Duplicate claim exposed or replaced the agent lease'; end if;
  begin
    perform public.cm_command_begin_agent(owner_a, request || '{"agent":"coo"}');
    raise exception 'Changed task reused an agent claim';
  exception when sqlstate 'CM006' then null;
  end;
  request := jsonb_build_object('id',run_id,'lease',lease,'output','{"draft":"Test agent result"}');
  begin
    perform public.cm_command_finish_agent(owner_a, request || jsonb_build_object('lease',gen_random_uuid()));
    raise exception 'Invalid agent lease accepted a result';
  exception when sqlstate 'CM007' then null;
  end;
  perform public.cm_command_finish_agent(owner_a, request);
  result := public.cm_command_finish_agent(owner_a, request);
  if result->>'status' <> 'succeeded' or result ? 'lease' or result->>'output' is null then
    raise exception 'Agent result was not safely persisted';
  end if;
  for index in 1 .. 29 loop
    perform public.cm_command_begin_agent(owner_a, jsonb_build_object('dedupe_key','agent-' || index,'agent','ceo','brief','Additional test'));
  end loop;
  if public.cm_command_begin_agent(owner_a, '{"dedupe_key":"agent-first","agent":"ceo","brief":"Summarize my priorities"}')->>'claimed' <> 'false' then
    raise exception 'Cost cap prevented an idempotent lookup';
  end if;
  begin
    perform public.cm_command_begin_agent(owner_a, '{"dedupe_key":"agent-limit","agent":"ceo","brief":"Exceeds cap"}');
    raise exception 'Rolling agent budget limit accepted too many requests';
  exception when sqlstate 'CM009' then null;
  end;
end;
$$;

reset role;
-- Force a write error to exercise durable retries in a rolled-back test transaction.
create function pg_temp.reject_automation_artifact() returns trigger language plpgsql as $$
begin
  if new.area = 'health' then raise exception using errcode = 'CM010', message = 'Test-only failure'; end if;
  return new;
end;
$$;
create trigger test_reject_automation_artifact before insert on cm_command.records
  for each row execute function pg_temp.reject_automation_artifact();
set local role service_role;

do $$
declare
  owner_a uuid := gen_random_uuid();
  state jsonb;
begin
  perform public.cm_command_mutate(owner_a, '{"kind":"set_automation","key":"engineering-monitor","paused":false,"interval_minutes":60}');
  state := public.cm_command_mutate(owner_a, '{"kind":"run_automation","key":"engineering-monitor","event_key":"known-failure"}');
  if state #>> '{runs,0,status}' <> 'retrying' or state #>> '{runs,0,retry_at}' is null then
    raise exception 'Failure did not record a retry';
  end if;
  perform public.cm_command_mutate(owner_a, '{"kind":"set_automation","key":"engineering-monitor","paused":true,"interval_minutes":60}');
  update cm_command.runs set retry_at = now() - interval '1 minute' where owner_id = owner_a;
  if public.cm_command_tick(owner_a)->>'processed' <> '0' then raise exception 'Paused workflow retried'; end if;
  perform public.cm_command_mutate(owner_a, '{"kind":"set_automation","key":"engineering-monitor","paused":false,"interval_minutes":60}');
  perform public.cm_command_tick(owner_a);
  update cm_command.runs set retry_at = now() - interval '1 minute' where owner_id = owner_a;
  perform public.cm_command_tick(owner_a);
  state := public.cm_command_state(owner_a);
  if state #>> '{runs,0,status}' <> 'failed' or state #>> '{runs,0,attempts}' <> '3' or
     not exists (select from jsonb_array_elements(state->'audit') item where item->>'event' = 'automation.failed') or
     jsonb_array_length(state->'records') <> 0 then
    raise exception 'Terminal failure, attempt count, alert or rollback was incorrect';
  end if;
end;
$$;

rollback;
