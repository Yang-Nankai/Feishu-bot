import cloud from '@lafjs/cloud'
import axios from 'axios'
// import * as  openai from "openai";
import OpenAI from 'openai';
const db = cloud.database()

const FeishuAppId = cloud.env.LARK_APPID;
const FeishuAppSecret = cloud.env.LARK_SECRET;

const waitReply = async (content) => {
  const message = "Test a Test";
  return message;
};

// 获取飞书 tenant_access_token 的方法
const getTenantToken = async () => {
  const url = 'https://open.feishu.cn/open-apis/v3/auth/tenant_access_token/internal/';
  const res = await axios.post(url, {
    'app_id': FeishuAppId,
    'app_secret': FeishuAppSecret,
  });

  return res.data.tenant_access_token;
};

const feishuReply = async (objs) => {
  const tenantToken = await getTenantToken();
  const url = `https://open.feishu.cn/open-apis/im/v1/messages/${objs.msgId}/reply`;
  let content = objs.content;
  if (objs.openId) content = `<at user_id="${objs.openId}"></at> ${content}`;
  const res = await axios({
    url, method: 'post',
    headers: { 'Authorization': `Bearer ${tenantToken}` },
    data: { msg_type: 'text', content: JSON.stringify({ text: content }) },
  });

  return res.data.data;
};

export async function main(ctx: FunctionContext) {

  const { body } = ctx

  if (body.challenge) return { challenge: body.challenge };

  const eventId = body.header.event_id;
  const contentsTable = db.collection('contents')
  const contentObj = await contentsTable.where({ eventId }).getOne();
  if (contentObj.data) return;

  const message = body.event.message;

  const messageContent = JSON.parse(message.content)
  let content = messageContent?.text?.replace('@_user_1 ', '') || '';
  if (!content) return

  const sender = body.event.sender;
  await contentsTable.add({
    eventId: body.header.event_id,
    msgId: message.message_id,
    openId: sender.sender_id.open_id,
    content,
    date: Date.now()
  });

  let replyContent = content;
  // const result = await waitReply(content);
  // replyContent = `${result.data.choices[0].message.content.trim()}`;
  replyContent = await waitReply(content);

  await feishuReply({
    msgId: message.message_id,
    openId: sender.sender_id.open_id,
    content: replyContent,
  });
}
