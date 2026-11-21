import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  listCommandIntegrations, readCommandIntegration, startCommandIntegrationAuthorization,
  verifyCommandIntegration,
} from '@/lib/command-integrations';

const owner = 'test-command-owner';
const businessEmail = 'owner@example.test';
const authConfigId = 'ac_test';
const accountId = 'ca_test';
const google = 'https://www.googleapis.com/auth/';
const fetchMock = vi.fn<typeof fetch>();

function response(value: unknown, status = 200, headers?: HeadersInit) {
  return new Response(JSON.stringify(value), { status, headers });
}

function account(toolkit: string, overrides: Record<string, unknown> = {}) {
  return {
    id: accountId, status: 'ACTIVE', user_id: owner, toolkit: { slug: toolkit },
    auth_config: { id: authConfigId, is_disabled: false }, is_disabled: false,
    state: { opaque: 'private-response-field' }, ...overrides,
  };
}

function config(toolkit: string, scope: string) {
  return { id: authConfigId, status: 'ENABLED', auth_scheme: 'OAUTH2', toolkit: { slug: toolkit }, credentials: { scopes: `${google}${scope}` } };
}

function prepare(toolkit: string) {
  vi.stubEnv('COMPOSIO_API_KEY', 'private-project-key');
  vi.stubEnv('COMPOSIO_GOOGLE_ACCOUNT_EMAIL', businessEmail);
  vi.stubEnv(`COMPOSIO_${toolkit.toUpperCase()}_AUTH_CONFIG_ID`, authConfigId);
}

function request(index: number) {
  const [url, options] = fetchMock.mock.calls[index];
  return { url: new URL(String(url)), options, body: options?.body ? JSON.parse(String(options.body)) : undefined };
}

beforeEach(() => {
  vi.stubGlobal('fetch', fetchMock);
  for (const slug of ['GMAIL', 'GOOGLECALENDAR', 'GOOGLEDRIVE', 'YOUTUBE']) {
    vi.stubEnv(`COMPOSIO_${slug}_AUTH_CONFIG_ID`, undefined);
    vi.stubEnv(`COMPOSIO_${slug}_CONNECTED_ACCOUNT_ID`, undefined);
  }
  for (const key of ['COMPOSIO_API_KEY', 'COMPOSIO_USER_ID', 'COMPOSIO_GOOGLE_ACCOUNT_EMAIL', 'COMPOSIO_YOUTUBE_CHANNEL_ID']) {
    vi.stubEnv(key, undefined);
  }
});

afterEach(() => {
  fetchMock.mockReset();
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

describe('Command Center Composio registry', () => {
  it('reports missing project configuration without making provider calls', async () => {
    const rows = await listCommandIntegrations(owner);
    expect(rows.find(row => row.id === 'gmail')).toMatchObject({ status: 'Not Configured', canAuthorize: false });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('creates a hosted Connect Link for the authenticated owner and the read-only auth config', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response(config('gmail', 'gmail.readonly')))
      .mockResolvedValueOnce(response({ items: [] }))
      .mockResolvedValueOnce(response({ redirect_url: 'https://connect.composio.dev/link/ln_test', link_token: 'private-link-token' }, 201));
    expect(await startCommandIntegrationAuthorization(owner, 'gmail')).toEqual({ authorizationUrl: 'https://connect.composio.dev/link/ln_test' });
    const list = request(1);
    expect(list.url.searchParams.get('user_ids')).toBe(owner);
    expect(list.url.searchParams.get('account_type')).toBe('PRIVATE');
    expect(request(2).url.pathname).toBe('/api/v3.1/connected_accounts/link');
    expect(request(2).body).toEqual({ user_id: owner, auth_config_id: authConfigId });
  });

  it('rejects an untrusted Connect Link redirect', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response(config('gmail', 'gmail.readonly')))
      .mockResolvedValueOnce(response({ items: [] }))
      .mockResolvedValueOnce(response({ redirect_url: 'https://connect.composio.dev.example.test/link/ln_test' }, 201));
    await expect(startCommandIntegrationAuthorization(owner, 'gmail')).rejects.toMatchObject({ status: 502 });
  });

  it('rejects write scope in a configured read-only OAuth connector before link creation', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response(config('gmail', 'gmail.readonly https://mail.google.com/')));
    await expect(startCommandIntegrationAuthorization(owner, 'gmail')).rejects.toMatchObject({ status: 409 });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('does not accept an account returned for another owner', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response({ items: [account('gmail', { user_id: 'another-owner' })] }));
    const result = await verifyCommandIntegration(owner, 'gmail');
    expect(result.status).toBe('Pending Authorization');
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('does not select between multiple active connections', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response({ items: [account('gmail'), account('gmail', { id: 'ca_other' })] }));
    const result = await verifyCommandIntegration(owner, 'gmail');
    expect(result).toMatchObject({ status: 'Failed', detail: expect.stringContaining('Multiple active accounts') });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('does not read inbox data when the mailbox identity disagrees', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response({ items: [account('gmail')] }))
      .mockResolvedValueOnce(response(config('gmail', 'gmail.readonly')))
      .mockResolvedValueOnce(response({ status: 200, data: { emailAddress: 'different@example.test' } }));
    await expect(readCommandIntegration(owner, 'gmail')).rejects.toMatchObject({ status: 409 });
    expect(fetchMock).toHaveBeenCalledTimes(3);
    expect(request(2).body).toMatchObject({ user_id: owner, connected_account_id: accountId, method: 'GET' });
    expect(request(2).body.endpoint).toContain('/profile');
  });

  it('verifies active connections on a registry refresh without reading inbox content', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response({ items: [account('gmail')] }))
      .mockResolvedValueOnce(response(config('gmail', 'gmail.readonly')))
      .mockResolvedValueOnce(response({ status: 200, data: { emailAddress: businessEmail } }));
    const rows = await listCommandIntegrations(owner);
    expect(rows.find(row => row.id === 'gmail')).toMatchObject({ status: 'Verified', verifiedAt: expect.any(String) });
    expect(fetchMock).toHaveBeenCalledTimes(3);
    expect(request(2).body.endpoint).toContain('/profile');
  });

  it('previews a verified Gmail inbox without returning full messages or headers', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response({ items: [account('gmail')] }))
      .mockResolvedValueOnce(response(config('gmail', 'gmail.readonly')))
      .mockResolvedValueOnce(response({ status: 200, data: { emailAddress: businessEmail } }))
      .mockResolvedValueOnce(response({ status: 200, data: { messages: [{ id: 'm1' }] } }))
      .mockResolvedValueOnce(response({ status: 200, data: {
        snippet: 'Looking forward to the session.', internalDate: '1795226400000',
        payload: { headers: [{ name: 'Subject', value: 'Workshop' }, { name: 'From', value: 'Coordinator' }, { name: 'BCC', value: 'private-recipient' }], body: 'private-body' },
      } }));
    const result = await readCommandIntegration(owner, 'gmail');
    expect(result.items).toMatchObject([{ id: 'm1', title: 'Workshop', detail: 'Coordinator · Looking forward to the session.', date: expect.any(String) }]);
    expect(JSON.stringify(result)).not.toContain('private');
    expect(request(4).body.parameters).toContainEqual({ name: 'format', value: 'metadata', type: 'query' });
  });

  it('returns sanitized metadata after a read-only Drive identity check', async () => {
    prepare('googledrive');
    fetchMock.mockResolvedValueOnce(response({ items: [account('googledrive')] }))
      .mockResolvedValueOnce(response(config('googledrive', 'drive.metadata.readonly')))
      .mockResolvedValueOnce(response({ status: 200, data: { user: { emailAddress: businessEmail } } }))
      .mockResolvedValueOnce(response({ status: 200, data: { files: [{ id: 'file-1', name: 'Assets', webViewLink: 'https://untrusted.example.test/', mimeType: 'text/plain' }] } }));
    const result = await readCommandIntegration(owner, 'googledrive');
    expect(result).toMatchObject({ integration: { status: 'Verified', verifiedAt: expect.any(String) }, items: [{ id: 'file-1', title: 'Assets', url: 'https://drive.google.com/open?id=file-1' }] });
    expect(JSON.stringify(result)).not.toMatch(/private|untrusted/);
    expect(request(3).body).toMatchObject({ method: 'GET', endpoint: 'https://www.googleapis.com/drive/v3/files' });
  });

  it('returns upcoming primary calendar events and preserves date-only events', async () => {
    prepare('googlecalendar');
    fetchMock.mockResolvedValueOnce(response({ items: [account('googlecalendar')] }))
      .mockResolvedValueOnce(response(config('googlecalendar', 'calendar.readonly')))
      .mockResolvedValueOnce(response({ status: 200, data: { id: businessEmail, primary: true } }))
      .mockResolvedValueOnce(response({ status: 200, data: { items: [
        { id: 'first', summary: 'Recording day', start: { date: '2026-11-23' } },
        { id: 'second', summary: 'Cancelled event', status: 'cancelled' },
      ] } }));
    expect((await readCommandIntegration(owner, 'googlecalendar')).items).toEqual([
      { id: 'first', title: 'Recording day', date: '2026-11-23', detail: 'All-day event' },
    ]);
    expect(request(3).body.parameters).toContainEqual({ name: 'orderBy', value: 'startTime', type: 'query' });
  });

  it('uses only the expected owned YouTube channel’s uploads playlist', async () => {
    prepare('youtube');
    vi.stubEnv('COMPOSIO_YOUTUBE_CHANNEL_ID', 'UC-expected');
    const channel = (id: string, uploads: string) => ({ id, contentDetails: { relatedPlaylists: { uploads } } });
    fetchMock.mockResolvedValueOnce(response({ items: [account('youtube')] }))
      .mockResolvedValueOnce(response(config('youtube', 'youtube.readonly')))
      .mockResolvedValueOnce(response({ status: 200, data: { items: [channel('UC-other', 'incorrect'), channel('UC-expected', 'expected')] } }))
      .mockResolvedValueOnce(response({ status: 200, data: { items: [{ snippet: { title: 'An episode' }, contentDetails: { videoId: 'video123' } }] } }));
    expect((await readCommandIntegration(owner, 'youtube')).items).toMatchObject([
      { id: 'video123', title: 'An episode', url: 'https://www.youtube.com/watch?v=video123' },
    ]);
    expect(request(3).body.parameters).toContainEqual({ name: 'playlistId', value: 'expected', type: 'query' });
  });

  it('treats a provider 403 inside a successful proxy HTTP response as failure', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response({ items: [account('gmail')] }))
      .mockResolvedValueOnce(response(config('gmail', 'gmail.readonly')))
      .mockResolvedValueOnce(response({ status: 403, data: { emailAddress: businessEmail, error: 'private-provider-error' } }));
    const result = await verifyCommandIntegration(owner, 'gmail');
    expect(result).toMatchObject({ status: 'Failed' });
    expect(JSON.stringify(result)).not.toContain('private-provider-error');
  });

  it('honors the provider retry delay and stops after a Composio rate limit', async () => {
    prepare('gmail');
    fetchMock.mockResolvedValueOnce(response({ error: 'private-provider-error' }, 429, { 'retry-after': '31' }));
    await expect(startCommandIntegrationAuthorization(owner, 'gmail')).rejects.toMatchObject({ status: 429, retryAfter: 31 });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
