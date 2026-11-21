const composioBaseUrl = 'https://backend.composio.dev/api/v3.1';
const googleScope = 'https://www.googleapis.com/auth/';
const previewSize = 6;

type Group = 'Google' | 'Development' | 'Business' | 'Social';
type Status = 'Verified' | 'Pending Authorization' | 'Not Configured' | 'Unsupported' | 'Failed';
type JsonObject = Record<string, unknown>;

export type CommandIntegration = {
  id: string;
  name: string;
  group: Group;
  provider: string;
  status: Status;
  detail: string;
  canAuthorize: boolean;
  canVerify: boolean;
  permissions: string[];
  limitation: string;
  verifiedAt?: string;
};

export type CommandIntegrationItem = {
  id: string;
  title: string;
  detail?: string;
  date?: string;
  url?: string;
};

type Connector = {
  name: string;
  permissions: string[];
  limitation: string;
};

const connectors = {
  gmail: {
    name: 'Gmail',
    permissions: [`${googleScope}gmail.readonly`],
    limitation: 'Verifies the mailbox and reads recent inbox subjects, senders, and snippets. Drafts are prepared in the command center. Gmail write access is disabled.',
  },
  googlecalendar: {
    name: 'Google Calendar',
    permissions: [`${googleScope}calendar.readonly`],
    limitation: 'Verifies the primary calendar and lists upcoming events. Invitations and calendar writes are disabled.',
  },
  googledrive: {
    name: 'Google Drive',
    permissions: [`${googleScope}drive.metadata.readonly`],
    limitation: 'Verifies the Drive account and reads recently modified file metadata. File content and writes are disabled.',
  },
  youtube: {
    name: 'YouTube',
    permissions: [`${googleScope}youtube.readonly`],
    limitation: 'Verifies the channel and reads recent uploads and available channel totals. Studio analytics, uploading, and publishing require separate authorization.',
  },
} satisfies Record<string, Connector>;

type ConnectorId = keyof typeof connectors;

type ConnectorConfig = {
  id: ConnectorId;
  apiKey: string;
  userId: string;
  authConfigId: string;
  connectedAccountId?: string;
  expectedIdentity: string;
};

type Account = { id: string; status: string };

const otherIntegrations: { id: string; name: string; group: Group; provider?: string; limitation: string }[] = [
  { id: 'googledocs', name: 'Google Docs', group: 'Google', limitation: 'Composio OAuth toolkit documented. Document access and editing require a separately scoped connector.' },
  { id: 'googlesheets', name: 'Google Sheets', group: 'Google', limitation: 'Composio OAuth toolkit documented. Sheet-level access has not been configured.' },
  { id: 'github', name: 'GitHub', group: 'Development', limitation: 'Composio OAuth toolkit documented. Command center access needs a repository-scoped connector.' },
  { id: 'netlify', name: 'Netlify', group: 'Development', provider: 'Netlify API', limitation: 'Use the official Netlify API for deployment monitoring. A Composio toolkit was not confirmed.' },
  { id: 'supabase', name: 'Supabase management', group: 'Development', limitation: 'Composio OAuth and API key options are documented. Live project discovery requires separately scoped access.' },
  { id: 'codex', name: 'Codex', group: 'Development', provider: 'GitHub / OpenAI', limitation: 'Use the repository development workflow and verified CI evidence. Remote Codex orchestration is not connected.' },
  { id: 'notion', name: 'Notion', group: 'Business', limitation: 'Composio OAuth and API key options are documented. Page access needs to be approved for this workspace.' },
  { id: 'crm', name: 'External CRM', group: 'Business', provider: 'Provider pending', limitation: 'The command center maintains local CRM records. An external system has not been selected.' },
  { id: 'scheduling', name: 'Scheduling platform', group: 'Business', provider: 'Provider pending', limitation: 'Google Calendar covers read-only scheduling. An external booking system has not been selected.' },
  { id: 'email-marketing', name: 'Email marketing', group: 'Business', provider: 'Provider pending', limitation: 'A marketing provider and approved audience have not been selected.' },
  { id: 'stripe', name: 'Stripe', group: 'Business', limitation: 'Composio OAuth and API key options are documented. Financial reporting requires a separately scoped account. Payments and subscriptions are disabled.' },
  { id: 'instagram', name: 'Instagram', group: 'Social', limitation: 'Composio OAuth toolkit documented. Capabilities depend on account type, provider app review, and permission grants.' },
  { id: 'facebook', name: 'Facebook', group: 'Social', limitation: 'Composio OAuth toolkit documented. Page access depends on account permissions and provider app review.' },
  { id: 'tiktok', name: 'TikTok', group: 'Social', limitation: 'Composio OAuth toolkit documented. Media actions have separate permissions and platform restrictions.' },
  { id: 'linkedin', name: 'LinkedIn', group: 'Social', limitation: 'Composio OAuth toolkit documented. Member and organization permissions need separate verification.' },
];

export class CommandIntegrationError extends Error {
  constructor(public status: number, message: string, public retryAfter?: number) {
    super(message);
    this.name = 'CommandIntegrationError';
  }
}

function asObject(value: unknown): JsonObject {
  return value !== null && typeof value === 'object' && !Array.isArray(value) ? value as JsonObject : {};
}

function asList(value: unknown): JsonObject[] {
  return Array.isArray(value) ? value.map(asObject) : [];
}

function asText(value: unknown): string {
  return typeof value === 'string' ? value : '';
}

function accountSetup(id: ConnectorId, ownerId: string): ConnectorConfig | undefined {
  const prefix = `COMPOSIO_${id.toUpperCase()}_`;
  const apiKey = process.env.COMPOSIO_API_KEY?.trim();
  const authConfigId = process.env[`${prefix}AUTH_CONFIG_ID`]?.trim();
  const connectedAccountId = process.env[`${prefix}CONNECTED_ACCOUNT_ID`]?.trim();
  const expectedIdentity = id === 'youtube'
    ? process.env.COMPOSIO_YOUTUBE_CHANNEL_ID?.trim()
    : process.env.COMPOSIO_GOOGLE_ACCOUNT_EMAIL?.trim().toLowerCase();
  if (!apiKey || !authConfigId || !expectedIdentity) return;
  return {
    id, apiKey, authConfigId, connectedAccountId, expectedIdentity,
    userId: process.env.COMPOSIO_USER_ID?.trim() || ownerId,
  };
}

function connectorId(key: string): ConnectorId {
  if (!Object.hasOwn(connectors, key)) throw new CommandIntegrationError(404, 'This integration has no implemented authorization flow.');
  return key as ConnectorId;
}

function requiredConfig(key: string, ownerId: string): ConnectorConfig {
  const config = accountSetup(connectorId(key), ownerId);
  if (!config) throw new CommandIntegrationError(503, 'Set the Composio project key, read-only auth config, and expected account identity on the server.');
  return config;
}

function providerFailure(status: number, retryAfter?: number): CommandIntegrationError {
  if (status === 429) return new CommandIntegrationError(429, 'The provider rate limit was reached. Try the action again after the retry period.', retryAfter);
  if (status === 401 || status === 403) return new CommandIntegrationError(502, 'The provider denied access. Check the project key, auth configuration, scopes, and connection.');
  return new CommandIntegrationError(502, 'The provider request failed. Check the connection and try again.');
}

async function composio(config: ConnectorConfig, path: string, body?: JsonObject): Promise<JsonObject> {
  let response: Response;
  try {
    response = await fetch(`${composioBaseUrl}${path}`, {
      method: body ? 'POST' : 'GET',
      headers: { 'x-api-key': config.apiKey, ...(body ? { 'Content-Type': 'application/json' } : {}) },
      body: body ? JSON.stringify(body) : undefined,
      cache: 'no-store',
      redirect: 'error',
      signal: AbortSignal.timeout(8000),
    });
  } catch {
    throw new CommandIntegrationError(502, 'The connection to Composio failed or timed out.');
  }
  if (!response.ok) {
    const retryAfter = response.headers.get('retry-after');
    throw providerFailure(response.status, retryAfter && /^\d+$/.test(retryAfter) ? Number(retryAfter) : undefined);
  }
  try {
    return asObject(await response.json());
  } catch {
    throw new CommandIntegrationError(502, 'Composio returned an unreadable response.');
  }
}

async function accounts(config: ConnectorConfig): Promise<Account[]> {
  const params = new URLSearchParams({
    toolkit_slugs: config.id, user_ids: config.userId, auth_config_ids: config.authConfigId,
    limit: '25', account_type: 'PRIVATE',
  });
  if (config.connectedAccountId) params.set('connected_account_ids', config.connectedAccountId);
  const result = await composio(config, `/connected_accounts?${params}`);
  if (!Array.isArray(result.items) || result.next_cursor) {
    throw new CommandIntegrationError(502, 'Account selection could not be verified. Pin the intended connected account in server configuration.');
  }
  return asList(result.items).flatMap(item => {
    const authConfig = asObject(item.auth_config);
    const accountType = asObject(item.experimental).account_type;
    if (asObject(item.toolkit).slug !== config.id || authConfig.id !== config.authConfigId ||
        (item.user_id && item.user_id !== config.userId) || (accountType && accountType !== 'PRIVATE') ||
        item.is_disabled || authConfig.is_disabled || (config.connectedAccountId && config.connectedAccountId !== item.id)) return [];
    const id = asText(item.id);
    const status = asText(item.status);
    return id && status ? [{ id, status }] : [];
  });
}

function activeAccount(matches: Account[]): Account | undefined {
  const active = matches.filter(account => account.status === 'ACTIVE');
  if (active.length > 1) throw new CommandIntegrationError(409, 'Multiple active accounts matched. Pin the intended connected account in server configuration.');
  return active[0];
}

async function checkReadOnlyConfig(config: ConnectorConfig): Promise<void> {
  const result = await composio(config, `/auth_configs/${encodeURIComponent(config.authConfigId)}`);
  if (result.id !== config.authConfigId || result.status !== 'ENABLED' || result.auth_scheme !== 'OAUTH2' ||
      asObject(result.toolkit).slug !== config.id) {
    throw new CommandIntegrationError(409, 'Enable the correct OAuth auth configuration in the Composio project.');
  }
  const configured = asObject(result.credentials).scopes;
  const scopes = Array.isArray(configured) ? configured : asText(configured).split(/[\s,]+/).filter(Boolean);
  const allowedScopes = new Set([...connectors[config.id].permissions, 'openid', 'email', 'profile', `${googleScope}userinfo.email`, `${googleScope}userinfo.profile`]);
  if (!connectors[config.id].permissions.every(scope => scopes.includes(scope)) || scopes.some(scope => !allowedScopes.has(scope))) {
    throw new CommandIntegrationError(409, 'Create a dedicated OAuth configuration with the listed read-only scopes. Review Google consent and reconnect if scopes changed.');
  }
}

function row(id: ConnectorId, status: Status, detail: string, options: Partial<Pick<CommandIntegration, 'canAuthorize'|'canVerify'|'verifiedAt'>> = {}): CommandIntegration {
  return {
    id, group: 'Google', provider: 'Composio', ...connectors[id], status, detail,
    canAuthorize: false, canVerify: false, ...options,
  };
}

function inactiveStatus(config: ConnectorConfig, matches: Account[]): CommandIntegration {
  if (matches.some(account => ['FAILED', 'EXPIRED', 'REVOKED'].includes(account.status))) {
    return row(config.id, 'Failed', 'The matching connection failed, expired, or was revoked. Reauthorize or update the server-pinned connection.', { canAuthorize: !config.connectedAccountId });
  }
  return row(config.id, 'Pending Authorization', 'Open a Composio Connect Link and authorize the intended business account.', { canAuthorize: !config.connectedAccountId, canVerify: true });
}

export async function listCommandIntegrations(ownerId: string): Promise<CommandIntegration[]> {
  const active = await Promise.all((Object.keys(connectors) as ConnectorId[]).map(async id => {
    const config = accountSetup(id, ownerId);
    if (!config) return row(id, 'Not Configured', 'Set the project key, read-only auth config, and expected account identity on the server.');
    return verify(config);
  }));
  return [...active, ...otherIntegrations.map(({ provider = 'Composio', ...entry }): CommandIntegration => ({
    ...entry, provider, status: 'Not Configured', detail: 'No command center connector is enabled.',
    permissions: [], canAuthorize: false, canVerify: false,
  }))];
}

function authorizationUrl(value: unknown): string {
  try {
    const url = new URL(asText(value));
    if (url.origin === 'https://connect.composio.dev' && !url.username && !url.password && url.pathname.startsWith('/link/')) return url.toString();
  } catch {
    // Reject incomplete URLs and any origin outside Composio's hosted Connect Link.
  }
  throw new CommandIntegrationError(502, 'Composio did not return a valid hosted authorization URL.');
}

export async function startCommandIntegrationAuthorization(ownerId: string, key: string): Promise<{ authorizationUrl: string }> {
  const config = requiredConfig(key, ownerId);
  if (config.connectedAccountId) throw new CommandIntegrationError(409, 'Remove or update the server-pinned account before creating a new connection.');
  await checkReadOnlyConfig(config);
  if (activeAccount(await accounts(config))) throw new CommandIntegrationError(409, 'An active connection already exists. Verify or revoke it before creating another.');
  const result = await composio(config, '/connected_accounts/link', {
    auth_config_id: config.authConfigId, user_id: config.userId,
  });
  return { authorizationUrl: authorizationUrl(result.redirect_url) };
}

async function readProvider(config: ConnectorConfig, account: Account, endpoint: string, query: Record<string, string> = {}): Promise<JsonObject> {
  const response = await composio(config, '/tools/execute/proxy', {
    user_id: config.userId, connected_account_id: account.id, endpoint, method: 'GET',
    parameters: Object.entries(query).map(([name, value]) => ({ name, value, type: 'query' })),
  });
  const status = Number(response.status);
  if (!Number.isInteger(status) || status < 200 || status >= 300) throw providerFailure(status);
  if (!response.data || typeof response.data !== 'object' || Array.isArray(response.data)) {
    throw new CommandIntegrationError(502, 'The provider returned an unreadable read-only result.');
  }
  return asObject(response.data);
}

async function probe(config: ConnectorConfig, account: Account): Promise<JsonObject> {
  let result: JsonObject;
  let identity = '';
  switch (config.id) {
    case 'gmail':
      result = await readProvider(config, account, 'https://gmail.googleapis.com/gmail/v1/users/me/profile');
      identity = asText(result.emailAddress).toLowerCase();
      break;
    case 'googlecalendar':
      result = await readProvider(config, account, 'https://www.googleapis.com/calendar/v3/users/me/calendarList/primary');
      identity = result.primary === true ? asText(result.id).toLowerCase() : '';
      break;
    case 'googledrive':
      result = await readProvider(config, account, 'https://www.googleapis.com/drive/v3/about', { fields: 'user(emailAddress)' });
      identity = asText(asObject(result.user).emailAddress).toLowerCase();
      break;
    case 'youtube':
      result = await readProvider(config, account, 'https://www.googleapis.com/youtube/v3/channels', { part: 'id,contentDetails,statistics', mine: 'true' });
      result = asList(result.items).find(channel => channel.id === config.expectedIdentity) ?? {};
      identity = asText(result.id);
      break;
  }
  if (!identity || identity !== config.expectedIdentity) {
    throw new CommandIntegrationError(409, 'The read-only probe did not match the expected business account or YouTube channel. Review the connection before accessing its data.');
  }
  return result;
}

function verified(id: ConnectorId): CommandIntegration {
  return row(id, 'Verified', 'Composio is active and the provider read-only identity check matched the configured business account.', {
    canVerify: true, verifiedAt: new Date().toISOString(),
  });
}

async function verify(config: ConnectorConfig): Promise<CommandIntegration> {
  try {
    const matches = await accounts(config);
    const account = activeAccount(matches);
    if (!account) return inactiveStatus(config, matches);
    await checkReadOnlyConfig(config);
    await probe(config, account);
    return verified(config.id);
  } catch (error) {
    return row(config.id, 'Failed', error instanceof CommandIntegrationError ? error.message : 'The read-only verification failed.', { canVerify: true });
  }
}

export async function verifyCommandIntegration(ownerId: string, key: string): Promise<CommandIntegration> {
  return verify(requiredConfig(key, ownerId));
}

function isoDate(value: unknown): string | undefined {
  if (typeof value !== 'string' && typeof value !== 'number') return;
  if (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value)) return value;
  const timestamp = new Date(value);
  return Number.isNaN(timestamp.valueOf()) ? undefined : timestamp.toISOString();
}

async function inbox(config: ConnectorConfig, account: Account): Promise<CommandIntegrationItem[]> {
  const root = 'https://gmail.googleapis.com/gmail/v1/users/me/messages';
  const result = await readProvider(config, account, root, { labelIds: 'INBOX', maxResults: String(previewSize) });
  const messageIds = asList(result.messages).map(message => asText(message.id)).filter(Boolean).slice(0, previewSize);
  return Promise.all(messageIds.map(async id => {
    const message = await readProvider(config, account, `${root}/${encodeURIComponent(id)}`, { format: 'metadata' });
    const headers = asList(asObject(message.payload).headers);
    const header = (name: string) => asText(headers.find(entry => asText(entry.name).toLowerCase() === name)?.value);
    const detail = [header('from'), asText(message.snippet)].filter(Boolean).join(' · ').slice(0, 500);
    const internalDate = asText(message.internalDate);
    return { id, title: header('subject').slice(0, 240) || 'No subject', detail, date: internalDate ? isoDate(Number(internalDate)) : undefined };
  }));
}

async function calendar(config: ConnectorConfig, account: Account): Promise<CommandIntegrationItem[]> {
  const result = await readProvider(config, account, 'https://www.googleapis.com/calendar/v3/calendars/primary/events', {
    timeMin: new Date().toISOString(), singleEvents: 'true', orderBy: 'startTime', maxResults: String(previewSize),
    fields: 'items(id,summary,start,status)',
  });
  return asList(result.items).slice(0, previewSize).flatMap(item => {
    const id = asText(item.id);
    const start = asObject(item.start);
    if (!id || item.status === 'cancelled') return [];
    return [{ id, title: asText(item.summary).slice(0, 240) || 'Calendar event', date: isoDate(start.dateTime ?? start.date), detail: start.date ? 'All-day event' : undefined }];
  });
}

async function drive(config: ConnectorConfig, account: Account): Promise<CommandIntegrationItem[]> {
  const result = await readProvider(config, account, 'https://www.googleapis.com/drive/v3/files', {
    q: 'trashed = false', orderBy: 'modifiedTime desc', pageSize: String(previewSize), fields: 'files(id,name,mimeType,modifiedTime)',
  });
  return asList(result.files).slice(0, previewSize).flatMap(item => {
    const id = asText(item.id);
    if (!id) return [];
    return [{ id, title: asText(item.name).slice(0, 240) || 'Drive file', detail: asText(item.mimeType), date: isoDate(item.modifiedTime), url: `https://drive.google.com/open?id=${encodeURIComponent(id)}` }];
  });
}

async function youtube(config: ConnectorConfig, account: Account, channel: JsonObject): Promise<CommandIntegrationItem[]> {
  const playlistId = asText(asObject(asObject(channel.contentDetails).relatedPlaylists).uploads);
  if (!playlistId) throw new CommandIntegrationError(502, 'YouTube did not return the verified channel’s uploads playlist.');
  const result = await readProvider(config, account, 'https://www.googleapis.com/youtube/v3/playlistItems', {
    part: 'snippet,contentDetails', playlistId, maxResults: String(previewSize),
  });
  const videos = asList(result.items).slice(0, previewSize).flatMap(item => {
    const content = asObject(item.contentDetails);
    const id = asText(content.videoId);
    if (!id) return [];
    return [{ id, title: asText(asObject(item.snippet).title).slice(0, 240) || 'YouTube video', date: isoDate(content.videoPublishedAt), url: `https://www.youtube.com/watch?v=${encodeURIComponent(id)}` }];
  });
  const statistics = asObject(channel.statistics);
  const totals = [
    ['Views', statistics.viewCount],
    ['Videos', statistics.videoCount],
    ['Subscribers', statistics.hiddenSubscriberCount === false ? statistics.subscriberCount : undefined],
  ].flatMap(([label, value]) => typeof value === 'string' && /^\d{1,30}$/.test(value)
    ? [`${label} ${new Intl.NumberFormat('en-US').format(BigInt(value))}`] : []);
  if (!totals.length) return videos;
  return [{ id: config.expectedIdentity, title: 'Channel totals', detail: totals.join(' · '), url: `https://www.youtube.com/channel/${encodeURIComponent(config.expectedIdentity)}` }, ...videos];
}

export async function readCommandIntegration(ownerId: string, key: string): Promise<{ integration: CommandIntegration; items: CommandIntegrationItem[] }> {
  const config = requiredConfig(key, ownerId);
  const account = activeAccount(await accounts(config));
  if (!account) throw new CommandIntegrationError(409, 'Authorize the intended business account before reading its data.');
  await checkReadOnlyConfig(config);
  const identity = await probe(config, account);
  const readers = { gmail: inbox, googlecalendar: calendar, googledrive: drive, youtube };
  const items = await readers[config.id](config, account, identity);
  return { integration: verified(config.id), items };
}
