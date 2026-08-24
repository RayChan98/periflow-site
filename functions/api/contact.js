// CF Pages Function: /api/contact (periflow)
// 发信后端：Zoho Mail API (OAuth2) —— 2026-08-20 全站统一口径，禁 Resend/formsubmit/Web3Forms
// 凭证只走 CF 项目环境变量（Dashboard 设）：ZOHO_CLIENT_ID / ZOHO_CLIENT_SECRET / ZOHO_REFRESH_TOKEN / ZOHO_ACCOUNT_ID
// 缺配置 fail-closed 返回 mail_not_configured（不丢单不泄密）
// 坑：① 禁 Response.redirect（CF Function 抛 1101）→ 返 JSON，前端跳 thank-you
//     ② 禁 _routes.json 列 /api/*（405）→ 删掉用默认路由
//     ③ 禁硬编码 key（钉进 git 历史泄露）
export async function onRequest(context) {
  if (context.request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    const data = await context.request.formData();

    // honeypot：机器人填入则静默返成功（不真发信）
    if (data.get('botcheck')) {
      return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { 'content-type': 'application/json' } });
    }

    const name = (data.get('name') || '').toString().trim();
    const email = (data.get('email') || '').toString().trim();
    const company = (data.get('company') || '').toString().trim();
    const product = (data.get('product') || '').toString().trim();
    const quantity = (data.get('quantity') || '').toString().trim();
    const message = (data.get('message') || '').toString().trim();
    const source = (data.get('form_source') || 'website').toString().trim();

    const text = [
      `New inquiry — ${source}`,
      '━━━━━━━━━━━━━━━━━━━━',
      `Name: ${name || '(not provided)'}`,
      `Email: ${email || '(not provided)'}`,
      `Company: ${company || '(not provided)'}`,
      `Product: ${product || '(not specified)'}`,
      `Quantity: ${quantity || '(not specified)'}`,
      `Message:`,
      message || '(not provided)',
      '━━━━━━━━━━━━━━━━━━━━',
      `Visitor IP: ${context.request.headers.get('cf-connecting-ip') || 'unknown'}`,
      `User-Agent: ${context.request.headers.get('user-agent') || 'unknown'}`,
      `Referrer: ${context.request.headers.get('referer') || 'direct'}`,
      `Submitted (UTC): ${new Date().toISOString()}`,
    ].join('\n');

    const env = context.env;
    if (env.ZOHO_CLIENT_ID && env.ZOHO_CLIENT_SECRET && env.ZOHO_REFRESH_TOKEN && env.ZOHO_ACCOUNT_ID) {
      // === Zoho Mail API (OAuth2) ===
      const tokenRes = await fetch(
        'https://accounts.zoho.com/oauth/v2/token?refresh_token=' + encodeURIComponent(env.ZOHO_REFRESH_TOKEN) +
        '&client_id=' + encodeURIComponent(env.ZOHO_CLIENT_ID) +
        '&client_secret=' + encodeURIComponent(env.ZOHO_CLIENT_SECRET) +
        '&grant_type=refresh_token',
        { method: 'POST' }
      );
      if (!tokenRes.ok) {
        return new Response(JSON.stringify({ ok: false, error: 'zoho_token_failed', detail: String(tokenRes.status) }), { status: 502, headers: { 'content-type': 'application/json' } });
      }
      const tokenJson = await tokenRes.json();
      const accessToken = tokenJson.access_token;
      if (!accessToken) {
        return new Response(JSON.stringify({ ok: false, error: 'zoho_no_access_token' }), { status: 502, headers: { 'content-type': 'application/json' } });
      }

      const mailRes = await fetch('https://mail.zoho.com/api/accounts/' + env.ZOHO_ACCOUNT_ID + '/messages', {
        method: 'POST',
        headers: {
          'Authorization': 'Zoho-oauthtoken ' + accessToken,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fromAddress: env.ZOHO_FROM_EMAIL || 'inquiry@periflow.pages.dev',
          toAddress: env.ZOHO_TO_EMAIL || 'cj226144@gmail.com',
          subject: `New inquiry: ${name || 'anonymous'}${company ? ' (' + company + ')' : ''}`,
          content: text,
          mailFormat: 'plaintext',
        }),
      });
      if (!mailRes.ok) {
        const errBody = await mailRes.text();
        return new Response(JSON.stringify({ ok: false, error: 'zoho_mail_failed', detail: errBody.slice(0, 300) }), { status: 502, headers: { 'content-type': 'application/json' } });
      }
      return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { 'content-type': 'application/json' } });
    }

    // 缺配置：fail-closed（Function 在线但未配置，部署后去 Dashboard 设 env）
    return new Response(JSON.stringify({ ok: false, error: 'mail_not_configured' }), { status: 500, headers: { 'content-type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: 'server_error', detail: String(e).slice(0, 150) }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
}
