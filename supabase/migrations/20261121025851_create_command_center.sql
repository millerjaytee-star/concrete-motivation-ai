-- Isolated owner workspace for the Concrete Command Center.
create schema cm_command;
revoke all on schema cm_command from public, anon, authenticated;
grant usage on schema cm_command to service_role;

create function cm_command.stage_key(p_stage text)
returns text language sql immutable security invoker set search_path = ''
as $$
  select replace(replace(lower(p_stage), ' ', '_'), '-', '_');
$$;

create function cm_command.requires_evidence(p_area text, p_stage text)
returns boolean language sql immutable security invoker set search_path = ''
as $$
  select cm_command.stage_key(p_stage) in ('verified','verified_evidence_linked','published','uploaded','upload','sent','deployed','released','submitted','paid','live','succeeded','production','approved_for_release','device_tested','scheduled','resolved','analytics','improvement','guest_confirmed','reply_received','member_joined','member_at_risk','member_cancelled')
    or (p_area = 'nation' and cm_command.stage_key(p_stage) in ('ready','completed'));
$$;

create table cm_command.records (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null,
  area text not null check (area in ('executive','agents','email','youtube','social','podcast','partnerships','nation','curriculum','revenue','crm','calendar','library','analytics','integrations','health')),
  title text not null check (char_length(title) between 1 and 200),
  stage text not null check (stage ~ '^[A-Za-z0-9][A-Za-z0-9 _-]{0,59}$'),
  body text not null default '' check (char_length(body) <= 20000),
  evidence text not null default '' check (char_length(evidence) <= 4000),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (owner_id, id),
  check (not cm_command.requires_evidence(area, stage) or btrim(evidence) <> '')
);
create index cm_records_updated on cm_command.records (owner_id, updated_at desc, id);
create index cm_records_trigger on cm_command.records (owner_id, area, stage, created_at, id);

create table cm_command.approvals (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null,
  action text not null check (action in ('external_communication','publish_content','spend_money','change_pricing','production_database_change','delete_records','change_permissions','production_deploy','app_release_submission','sign_agreement','send_email','publish_youtube','calendar_invite')),
  title text not null check (char_length(title) between 1 and 200),
  body text not null default '' check (char_length(body) <= 20000),
  record_id uuid,
  dedupe_key text not null check (char_length(dedupe_key) between 1 and 200),
  status text not null default 'pending' check (status in ('pending','approved','rejected')),
  decision_note text not null default '' check (char_length(decision_note) <= 2000),
  created_at timestamptz not null default now(),
  decided_at timestamptz,
  unique (owner_id, dedupe_key),
  foreign key (owner_id, record_id) references cm_command.records (owner_id, id),
  check ((status = 'pending') = (decided_at is null))
);
create index cm_approvals_created on cm_command.approvals (owner_id, created_at desc, id);

create table cm_command.audit (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null,
  event text not null,
  subject_id uuid,
  details jsonb not null default '{}',
  created_at timestamptz not null default clock_timestamp()
);
create index cm_audit_created on cm_command.audit (owner_id, created_at desc, id);

create function cm_command.automation_defaults()
returns table (key text, interval_minutes integer)
language sql immutable security invoker set search_path = ''
as $$
  values ('daily-briefing', 1440), ('content-draft', 60), ('podcast-confirmation', 15),
    ('outreach-reply', 15), ('membership-event', 60), ('engineering-monitor', 60)
$$;

create table cm_command.automations (
  owner_id uuid not null,
  key text not null check (key in ('daily-briefing','content-draft','podcast-confirmation','outreach-reply','membership-event','engineering-monitor')),
  paused boolean not null default true,
  interval_minutes integer not null check (interval_minutes between 5 and 10080),
  next_run_at timestamptz,
  updated_at timestamptz not null default now(),
  primary key (owner_id, key),
  check (paused = (next_run_at is null))
);

create table cm_command.runs (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null,
  key text not null,
  event_key text not null check (char_length(event_key) between 1 and 240),
  source_id uuid,
  status text not null default 'running' check (status in ('running','succeeded','skipped','retrying','failed')),
  attempts integer not null default 1 check (attempts between 1 and 3),
  created_at timestamptz not null default now(),
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  retry_at timestamptz,
  output text,
  error text,
  unique (owner_id, key, event_key),
  foreign key (owner_id, key) references cm_command.automations (owner_id, key),
  foreign key (owner_id, source_id) references cm_command.records (owner_id, id)
);
create index cm_runs_created on cm_command.runs (owner_id, created_at desc, id);
create index cm_runs_retry on cm_command.runs (owner_id, retry_at, id) where status = 'retrying';

create table cm_command.agent_runs (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null,
  dedupe_key text not null check (char_length(dedupe_key) between 1 and 200),
  agent text not null check (char_length(agent) between 1 and 100),
  brief text not null check (char_length(brief) between 1 and 20000),
  lease uuid not null default gen_random_uuid(),
  status text not null default 'running' check (status in ('running','succeeded','failed','uncertain')),
  output text check (char_length(output) <= 100000),
  error text check (char_length(error) <= 2000),
  created_at timestamptz not null default now(),
  finished_at timestamptz,
  unique (owner_id, dedupe_key)
);
create index cm_agent_runs_created on cm_command.agent_runs (owner_id, created_at desc, id);

alter table cm_command.records enable row level security;
alter table cm_command.approvals enable row level security;
alter table cm_command.audit enable row level security;
alter table cm_command.automations enable row level security;
alter table cm_command.runs enable row level security;
alter table cm_command.agent_runs enable row level security;
revoke all on all tables in schema cm_command from public, anon, authenticated;
grant select, insert, update on cm_command.records, cm_command.approvals, cm_command.automations, cm_command.runs, cm_command.agent_runs to service_role;
grant select, insert on cm_command.audit to service_role;

create function cm_command.log_event(p_actor uuid, p_event text, p_subject uuid, p_details jsonb)
returns void language sql security invoker set search_path = ''
as $$
  insert into cm_command.audit (owner_id, event, subject_id, details) values (p_actor, p_event, p_subject, p_details);
$$;

create function cm_command.agent_view(p_run cm_command.agent_runs)
returns jsonb language sql stable security invoker set search_path = ''
as $$
  select to_jsonb(p_run) - array['owner_id', 'dedupe_key', 'lease'] ||
    case when p_run.status = 'running' and p_run.created_at < now() - interval '2 minutes'
      then jsonb_build_object('status', 'uncertain', 'error', 'The request timed out before its result was recorded.')
      else '{}'::jsonb end;
$$;

create function public.cm_command_state(p_actor uuid)
returns jsonb language sql stable security invoker set search_path = ''
as $$
  select jsonb_build_object(
    'records', coalesce((select jsonb_agg(to_jsonb(r) - 'owner_id' order by r.updated_at desc, r.id) from
      (select * from cm_command.records where owner_id = p_actor order by updated_at desc, id limit 200) r), '[]'::jsonb),
    'approvals', coalesce((select jsonb_agg(to_jsonb(a) - 'owner_id' order by (a.status = 'pending') desc, a.created_at desc, a.id) from
      (select * from cm_command.approvals where owner_id = p_actor order by (status = 'pending') desc, created_at desc, id limit 200) a), '[]'::jsonb),
    'audit', coalesce((select jsonb_agg(to_jsonb(a) - 'owner_id' order by a.created_at desc, a.id) from
      (select * from cm_command.audit where owner_id = p_actor order by created_at desc, id limit 100) a), '[]'::jsonb),
    'automations', coalesce((select jsonb_agg(jsonb_build_object('key', d.key, 'paused', coalesce(a.paused, true),
      'interval_minutes', coalesce(a.interval_minutes, d.interval_minutes), 'next_run_at', a.next_run_at, 'updated_at', a.updated_at) order by d.key)
      from cm_command.automation_defaults() d left join cm_command.automations a on a.owner_id = p_actor and a.key = d.key), '[]'::jsonb),
    'runs', coalesce((select jsonb_agg(to_jsonb(r) - array['owner_id','source_id'] order by r.created_at desc, r.id) from
      (select * from cm_command.runs where owner_id = p_actor order by created_at desc, id limit 100) r), '[]'::jsonb),
    'agent_runs', coalesce((select jsonb_agg(cm_command.agent_view(r) order by r.created_at desc, r.id) from
      (select * from cm_command.agent_runs where owner_id = p_actor order by created_at desc, id limit 20) r), '[]'::jsonb)
  );
$$;

create function cm_command.eligible_source(p_key text, p_area text, p_stage text, p_evidence text)
returns boolean language sql immutable security invoker set search_path = ''
as $$
  select case p_key
    when 'content-draft' then p_area = 'library' and cm_command.stage_key(p_stage) = 'approved_theme'
    when 'podcast-confirmation' then p_area = 'podcast' and cm_command.stage_key(p_stage) = 'guest_confirmed' and btrim(p_evidence) <> ''
    when 'outreach-reply' then p_area = 'crm' and cm_command.stage_key(p_stage) = 'reply_received' and btrim(p_evidence) <> ''
    when 'membership-event' then p_area = 'revenue' and cm_command.stage_key(p_stage) in ('member_joined','member_at_risk','member_cancelled') and btrim(p_evidence) <> ''
    else false
  end;
$$;

create function cm_command.run_automation(p_actor uuid, p_key text, p_event text, p_source uuid default null)
returns void language plpgsql security invoker set search_path = ''
as $$
declare
  v_run cm_command.runs%rowtype;
  v_source cm_command.records%rowtype;
  v_title text;
  v_area text;
  v_stage text := 'Draft';
  v_body text;
  v_rows text;
  v_error text;
  v_artifact uuid;
begin
  if p_source is not null and p_event <> 'record:' || p_source::text then
    raise exception using errcode = 'CM001', message = 'Noncanonical event identifier';
  end if;
  insert into cm_command.runs (owner_id, key, event_key, source_id)
    values (p_actor, p_key, p_event, p_source) on conflict (owner_id, key, event_key) do nothing returning * into v_run;
  if not found then
    update cm_command.runs set attempts = attempts + 1, status = 'running', started_at = now(), finished_at = null, retry_at = null, error = null
      where owner_id = p_actor and key = p_key and event_key = p_event and status = 'retrying' and retry_at <= now()
      returning * into v_run;
    if not found then return; end if;
  end if;

  begin
    if p_source is not null then
      select * into v_source from cm_command.records where owner_id = p_actor and id = p_source;
    end if;
    if p_key not in ('daily-briefing', 'engineering-monitor') and
       (v_source.id is null or not cm_command.eligible_source(p_key, v_source.area, v_source.stage, v_source.evidence)) then
      update cm_command.runs set status = 'skipped', finished_at = now(), output = 'No eligible source record was available.' where id = v_run.id;
      perform cm_command.log_event(p_actor, 'automation.skipped', v_run.id, jsonb_build_object('key', p_key));
      return;
    end if;

    case p_key
      when 'daily-briefing' then
        v_area := 'executive';
        v_title := 'Executive briefing · ' || (now() at time zone 'UTC')::date;
        select string_agg(format('- %s · %s (%s)', upper(r.area), r.title, r.stage), E'\n' order by r.area, r.updated_at desc, r.id)
          into v_rows from (
            select id, area, title, stage, updated_at from cm_command.records where owner_id = p_actor
              and area in ('calendar','email','youtube','social','library','podcast','partnerships','crm','nation','health')
              and updated_at >= now() - interval '7 days' order by updated_at desc, id limit 24
          ) r;
        v_body := format(E'Recent workspace records\n%s\n\nPending owner decisions: %s\n\nScope: workspace records updated in the last seven days.',
          coalesce(v_rows, 'No recent records in the connected workspace.'),
          (select count(*) from cm_command.approvals where owner_id = p_actor and status = 'pending'));
      when 'content-draft' then
        v_area := 'library';
        v_title := left('Draft package · ' || v_source.title, 200);
        v_body := 'Approved theme: ' || v_source.title || E'\n\n' || left(v_source.body, 12000) ||
          E'\n\nProduction brief\n- Audience: confirm the intended audience.\n- Message: connect this theme to the relevant Concrete Motivation pillar.\n- Deliverables: one long-form outline, one short-form script, one caption.\n- Review: fact-check sources, confirm asset rights, and request publishing approval.';
      when 'podcast-confirmation' then
        v_area := 'podcast';
        v_stage := 'Episode prep';
        v_title := left('Episode preparation · ' || v_source.title, 200);
        v_body := 'Guest confirmation record: ' || v_source.title || E'\n\n' || left(v_source.body, 12000) ||
          E'\n\nProduction checklist\n- Confirm recording dates and timezone.\n- Prepare a calendar proposal and guest release.\n- Research guest and write interview questions.\n- Check recording, transcription, rights, and distribution requirements.';
      when 'outreach-reply' then
        v_area := 'crm';
        v_stage := 'Follow-up';
        v_title := left('Review outreach reply · ' || v_source.title, 200);
        v_body := 'Reply record: ' || v_source.title || E'\n\n' || left(v_source.body, 12000) ||
          E'\n\nReview the reply for intent and deadlines, update the contact record, and prepare a response for owner approval.';
      when 'membership-event' then
        v_area := 'revenue';
        v_stage := 'Engagement draft';
        v_title := left('Membership follow-up · ' || v_source.title, 200);
        v_body := 'Membership event: ' || v_source.stage || E'\n\n' || left(v_source.body, 12000) ||
          E'\n\nReview the referenced event and prepare an appropriate onboarding, engagement, or retention response for owner approval.';
      when 'engineering-monitor' then
        v_area := 'health';
        v_title := 'Engineering review · ' || (now() at time zone 'UTC')::date;
        select string_agg(format('- %s (%s) · %s', r.title, r.stage, left(r.evidence, 160)), E'\n' order by r.updated_at desc, r.id)
          into v_rows from (
            select id, title, stage, evidence, updated_at from cm_command.records where owner_id = p_actor
              and area in ('nation','health') and stage in ('failed','blocked','defect','release_blocker')
              and updated_at >= now() - interval '7 days' and btrim(evidence) <> '' order by updated_at desc, id limit 24
          ) r;
        v_body := E'Evidence-backed engineering issues recorded in the last seven days\n' ||
          coalesce(v_rows, 'No evidence-backed issues were recorded in this period.');
    end case;

    insert into cm_command.records (owner_id, area, title, stage, body, evidence)
      values (p_actor, v_area, v_title, v_stage, v_body, case when p_source is null then '' else 'Workspace record ' || p_source::text end)
      returning id into v_artifact;
    update cm_command.runs set status = 'succeeded', finished_at = now(), output = v_title where id = v_run.id;
    perform cm_command.log_event(p_actor, 'automation.succeeded', v_run.id, jsonb_build_object('key', p_key, 'artifact_id', v_artifact));
  exception when others then
    v_error := SQLSTATE;
    update cm_command.runs set status = case when attempts >= 3 then 'failed' else 'retrying' end,
      finished_at = now(), retry_at = case when attempts < 3 then now() + make_interval(mins => attempts * 5) end,
      error = 'Workflow failed with database code ' || v_error where id = v_run.id;
    perform cm_command.log_event(p_actor, case when v_run.attempts >= 3 then 'automation.failed' else 'automation.retrying' end,
      v_run.id, jsonb_build_object('key', p_key, 'attempts', v_run.attempts, 'code', v_error));
  end;
end;
$$;

create function cm_command.tick_automations(p_actor uuid)
returns integer language plpgsql security invoker set search_path = ''
as $$
declare
  v_config cm_command.automations%rowtype;
  v_run cm_command.runs%rowtype;
  v_source uuid;
  v_work integer := 0;
  v_found integer;
begin
  for v_run in
    select r.* from cm_command.runs r join cm_command.automations a using (owner_id, key)
      where r.owner_id = p_actor and not a.paused and r.status = 'retrying' and r.retry_at <= now()
      order by r.retry_at, r.id limit 10
  loop
    perform cm_command.run_automation(p_actor, v_run.key, v_run.event_key, v_run.source_id);
    v_work := v_work + 1;
  end loop;

  for v_config in
    select * from cm_command.automations where owner_id = p_actor and not paused and next_run_at <= now() order by key
  loop
    if v_config.key in ('daily-briefing', 'engineering-monitor') then
      perform cm_command.run_automation(p_actor, v_config.key, 'scheduled:' || extract(epoch from v_config.next_run_at)::text);
      v_work := v_work + 1;
    else
      v_found := 0;
      for v_source in
        select r.id from cm_command.records r where r.owner_id = p_actor
          and cm_command.eligible_source(v_config.key, r.area, r.stage, r.evidence)
          and not exists (select 1 from cm_command.runs where owner_id = p_actor and key = v_config.key and event_key = 'record:' || r.id::text)
          order by r.created_at, r.id limit 10
      loop
        perform cm_command.run_automation(p_actor, v_config.key, 'record:' || v_source::text, v_source);
        v_work := v_work + 1;
        v_found := v_found + 1;
      end loop;
      if v_found = 0 then
        perform cm_command.run_automation(p_actor, v_config.key, 'scheduled:' || extract(epoch from v_config.next_run_at)::text);
        v_work := v_work + 1;
      end if;
    end if;
    update cm_command.automations set next_run_at = now() + make_interval(mins => v_config.interval_minutes)
      where owner_id = p_actor and key = v_config.key;
  end loop;
  return v_work;
end;
$$;

create function public.cm_command_tick(p_actor uuid)
returns jsonb language plpgsql security invoker set search_path = ''
as $$
begin
  if p_actor is null then raise exception using errcode = 'CM008', message = 'Missing workspace owner'; end if;
  perform pg_advisory_xact_lock(hashtextextended(p_actor::text, 71822));
  return jsonb_build_object('processed', cm_command.tick_automations(p_actor));
end;
$$;

create function public.cm_command_mutate(p_actor uuid, p_mutation jsonb)
returns jsonb language plpgsql security invoker set search_path = ''
as $$
declare
  v_id uuid;
  v_source uuid;
  v_area text := p_mutation->>'area';
  v_stage text := p_mutation->>'stage';
  v_action text := p_mutation->>'action';
  v_title text := btrim(p_mutation->>'title');
  v_evidence text := btrim(coalesce(p_mutation->>'evidence', ''));
  v_body text := coalesce(p_mutation->>'body', '');
  v_dedupe text := btrim(p_mutation->>'dedupe_key');
  v_decision text := p_mutation->>'decision';
  v_note text := btrim(coalesce(p_mutation->>'note', ''));
  v_key text := p_mutation->>'key';
  v_event text;
  v_interval integer;
  v_paused boolean;
  v_approval cm_command.approvals%rowtype;
  v_config cm_command.automations%rowtype;
  v_record cm_command.records%rowtype;
begin
  if p_actor is null then raise exception using errcode = 'CM008', message = 'Missing workspace owner'; end if;
  if jsonb_typeof(p_mutation) is distinct from 'object' then
    raise exception using errcode = 'CM001', message = 'Expected mutation object';
  end if;
  perform pg_advisory_xact_lock(hashtextextended(p_actor::text, 71822));

  case p_mutation->>'kind'
    when 'save_record' then
      if nullif(v_title,'') is null or v_area is null or v_stage is null then
        raise exception using errcode = 'CM001', message = 'Missing record fields';
      end if;
      if v_evidence = '' and cm_command.requires_evidence(v_area, v_stage) then
        raise exception using errcode = 'CM004', message = 'Source evidence required';
      end if;
      v_id := nullif(p_mutation->>'id', '')::uuid;
      if v_id is null then
        insert into cm_command.records (owner_id, area, title, stage, body, evidence)
          values (p_actor, v_area, v_title, v_stage, v_body, v_evidence) returning id into v_id;
        perform cm_command.log_event(p_actor, 'record.created', v_id, jsonb_build_object('area', v_area, 'stage', v_stage));
      else
        update cm_command.records set title = v_title, stage = v_stage, body = v_body, evidence = v_evidence, updated_at = now()
          where owner_id = p_actor and id = v_id and area = v_area;
        if not found then raise exception using errcode = 'CM002', message = 'Record not found in area'; end if;
        perform cm_command.log_event(p_actor, 'record.updated', v_id, jsonb_build_object('area', v_area, 'stage', v_stage));
      end if;
    when 'request_approval' then
      if nullif(v_title,'') is null or nullif(v_dedupe,'') is null or v_action is null then
        raise exception using errcode = 'CM001', message = 'Missing approval fields';
      end if;
      v_source := nullif(p_mutation->>'record_id', '')::uuid;
      if v_source is not null and not exists (select from cm_command.records where owner_id = p_actor and id = v_source) then
        raise exception using errcode = 'CM002', message = 'Source record not found';
      end if;
      insert into cm_command.approvals (owner_id, action, title, body, record_id, dedupe_key)
        values (p_actor, v_action, v_title, v_body, v_source, v_dedupe)
        on conflict (owner_id, dedupe_key) do nothing returning id into v_id;
      if found then
        perform cm_command.log_event(p_actor, 'approval.requested', v_id, jsonb_build_object('action', v_action, 'status', 'pending'));
      else
        select * into v_approval from cm_command.approvals where owner_id = p_actor and dedupe_key = v_dedupe;
        if row(v_action, v_title, v_body, v_source) is distinct from row(v_approval.action, v_approval.title, v_approval.body, v_approval.record_id) then
          raise exception using errcode = 'CM003', message = 'Approval key already describes a different action';
        end if;
      end if;
    when 'decide_approval' then
      if v_decision is null or v_decision not in ('approved', 'rejected') then
        raise exception using errcode = 'CM001', message = 'Invalid owner decision';
      end if;
      v_id := (p_mutation->>'id')::uuid;
      select * into v_approval from cm_command.approvals where owner_id = p_actor and id = v_id;
      if not found then raise exception using errcode = 'CM002', message = 'Approval not found'; end if;
      if v_approval.status = 'pending' then
        update cm_command.approvals set status = v_decision, decision_note = v_note, decided_at = now() where owner_id = p_actor and id = v_id;
        perform cm_command.log_event(p_actor, 'approval.decided', v_id, jsonb_build_object('action', v_approval.action, 'status', v_decision));
      elsif v_approval.status <> v_decision or v_approval.decision_note <> v_note then
        raise exception using errcode = 'CM003', message = 'Approval has already been decided';
      end if;
    when 'set_automation' then
      if not exists (select from cm_command.automation_defaults() where key = v_key)
        or jsonb_typeof(p_mutation->'paused') is distinct from 'boolean' or jsonb_typeof(p_mutation->'interval_minutes') is distinct from 'number' then
        raise exception using errcode = 'CM001', message = 'Invalid automation configuration';
      end if;
      v_interval := (p_mutation->>'interval_minutes')::integer;
      v_paused := (p_mutation->>'paused')::boolean;
      insert into cm_command.automations as a (owner_id, key, paused, interval_minutes, next_run_at)
        values (p_actor, v_key, v_paused, v_interval, case when not v_paused then now() + make_interval(mins => v_interval) end)
        on conflict (owner_id, key) do update set paused = excluded.paused, interval_minutes = excluded.interval_minutes,
          next_run_at = excluded.next_run_at, updated_at = now()
          where row(a.paused, a.interval_minutes) is distinct from row(excluded.paused, excluded.interval_minutes);
      if found then
        perform cm_command.log_event(p_actor, 'automation.configured', null, jsonb_build_object('key', v_key, 'paused', v_paused, 'interval_minutes', v_interval));
      end if;
    when 'run_automation' then
      if not exists (select from cm_command.automation_defaults() where key = v_key) then
        raise exception using errcode = 'CM001', message = 'Unknown automation';
      end if;
      select * into v_config from cm_command.automations where owner_id = p_actor and key = v_key;
      if not found or v_config.paused then raise exception using errcode = 'CM005', message = 'Automation is paused'; end if;
      v_source := (p_mutation #>> '{trigger,record_id}')::uuid;
      if v_source is not null then
        select * into v_record from cm_command.records where owner_id = p_actor and id = v_source;
        if not found then raise exception using errcode = 'CM002', message = 'Source record not found'; end if;
        if not cm_command.eligible_source(v_key, v_record.area, v_record.stage, v_record.evidence) then
          raise exception using errcode = 'CM001', message = 'Source record is not eligible for this automation';
        end if;
        v_event := 'record:' || v_source::text;
      else
        v_event := 'manual:' || nullif(btrim(p_mutation->>'event_key'),'');
      end if;
      if v_event is null or char_length(v_event) > 240 then
        raise exception using errcode = 'CM001', message = 'Invalid automation event identifier';
      end if;
      perform cm_command.run_automation(p_actor, v_key, v_event, v_source);
    when 'tick_automations' then
      perform cm_command.tick_automations(p_actor);
    else
      raise exception using errcode = 'CM001', message = 'Unknown workspace operation';
  end case;
  return public.cm_command_state(p_actor);
end;
$$;

create function public.cm_command_begin_agent(p_actor uuid, p_request jsonb)
returns jsonb language plpgsql security invoker set search_path = ''
as $$
declare
  v_key text := btrim(p_request->>'dedupe_key');
  v_agent text := btrim(p_request->>'agent');
  v_brief text := btrim(p_request->>'brief');
  v_run cm_command.agent_runs%rowtype;
begin
  if p_actor is null then raise exception using errcode = 'CM008', message = 'Missing workspace owner'; end if;
  if nullif(v_key,'') is null or nullif(v_agent,'') is null or nullif(v_brief,'') is null then
    raise exception using errcode = 'CM001', message = 'Missing agent request fields';
  end if;
  perform pg_advisory_xact_lock(hashtextextended(p_actor::text, 71822));
  select * into v_run from cm_command.agent_runs where owner_id = p_actor and dedupe_key = v_key;
  if found then
    if row(v_agent, v_brief) is distinct from row(v_run.agent, v_run.brief) then
      raise exception using errcode = 'CM006', message = 'Agent request identifier already used';
    end if;
    return jsonb_build_object('claimed', false, 'run', cm_command.agent_view(v_run));
  end if;
  if (select count(*) from cm_command.agent_runs where owner_id = p_actor and created_at > now() - interval '24 hours') >= 30 then
    raise exception using errcode = 'CM009', message = 'Rolling daily agent limit reached';
  end if;
  insert into cm_command.agent_runs (owner_id, dedupe_key, agent, brief) values (p_actor, v_key, v_agent, v_brief) returning * into v_run;
  perform cm_command.log_event(p_actor, 'agent.started', v_run.id, jsonb_build_object('agent', v_run.agent));
  return jsonb_build_object('claimed', true, 'lease', v_run.lease, 'run', cm_command.agent_view(v_run));
end;
$$;

create function public.cm_command_finish_agent(p_actor uuid, p_result jsonb)
returns jsonb language plpgsql security invoker set search_path = ''
as $$
declare
  v_run cm_command.agent_runs%rowtype;
  v_output text := nullif(p_result->>'output','');
  v_error text := nullif(p_result->>'error','');
begin
  if p_actor is null then raise exception using errcode = 'CM008', message = 'Missing workspace owner'; end if;
  if (v_output is null) = (v_error is null) then
    raise exception using errcode = 'CM001', message = 'Provide exactly one agent output or error';
  end if;
  perform pg_advisory_xact_lock(hashtextextended(p_actor::text, 71822));
  select * into v_run from cm_command.agent_runs where owner_id = p_actor and id = (p_result->>'id')::uuid;
  if not found then raise exception using errcode = 'CM002', message = 'Agent run not found'; end if;
  if v_run.lease is distinct from (p_result->>'lease')::uuid then
    raise exception using errcode = 'CM007', message = 'Agent run lease does not match';
  end if;
  if v_run.status = 'running' then
    update cm_command.agent_runs set status = case when v_error is null then 'succeeded' else 'failed' end,
      output = v_output, error = v_error, finished_at = now() where id = v_run.id returning * into v_run;
    perform cm_command.log_event(p_actor, 'agent.' || v_run.status, v_run.id, jsonb_build_object('agent', v_run.agent));
  elsif row(v_output, v_error) is distinct from row(v_run.output, v_run.error) then
    raise exception using errcode = 'CM007', message = 'Agent run already recorded a different result';
  end if;
  return cm_command.agent_view(v_run);
end;
$$;

revoke all on all functions in schema cm_command from public, anon, authenticated;
grant execute on all functions in schema cm_command to service_role;
revoke all on function public.cm_command_state(uuid), public.cm_command_mutate(uuid, jsonb), public.cm_command_tick(uuid),
  public.cm_command_begin_agent(uuid, jsonb), public.cm_command_finish_agent(uuid, jsonb) from public, anon, authenticated;
grant execute on function public.cm_command_state(uuid), public.cm_command_mutate(uuid, jsonb), public.cm_command_tick(uuid),
  public.cm_command_begin_agent(uuid, jsonb), public.cm_command_finish_agent(uuid, jsonb) to service_role;
