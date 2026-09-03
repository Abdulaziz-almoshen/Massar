-- QA seed. Written straight to the ledger so the transcript is deterministic and NO agent turn,
-- and therefore no send path, is involved in building the fixture.
DELETE FROM contacts; DELETE FROM messages; DELETE FROM interest_tags; DELETE FROM events;
DELETE FROM entities; DELETE FROM contact_insights;

-- A. the rich record used by smoke.py's landmark and by every pixel capture
INSERT INTO contacts (phone, wa_name, first_seen_at, last_event_at, status_times, outcome,
  outcome_reason, opted_out, human, agent_turns, test, scheduled_said, scheduled_at, outcome_evidence, props)
VALUES ('966500000850','د. سارة العتيبي',1786900000000,1786990000000,
  '{"sent":1786900001000,"delivered":1786900002000,"read":1786900050000,"replied":1786900400000}'::jsonb,
  'interested','أبدت اهتمامًا بالتكامل',false,false,2,false,
  'خلّها بكرة الصبح',1787040600000,'نبغى نعرف التكامل مع نظامنا','{}'::jsonb);
INSERT INTO messages (phone, role, text, ts) VALUES
 ('966500000850','agent','السلام عليكم، معك مساعد مسار من لين. نوفّر خدمة الإجازات المرضية الإلكترونية للمنشآت الصحية.',1786900300000),
 ('966500000850','customer','نبغى نعرف التكامل مع نظامنا',1786900400000),
 ('966500000850','agent','التكامل يتم عبر واجهات برمجية جاهزة مع أنظمة HIS، والتشغيل خلال أسبوعين.',1786900500000),
 ('966500000850','customer','والسعر كم؟ يحتاج موافقة الإدارة',1786900600000),
 ('966500000850','customer','خلّها بكرة الصبح',1786900700000);
INSERT INTO interest_tags (phone, product, level, ts) VALUES
 ('966500000850','الإجازات المرضية','hot',1786900650000);
INSERT INTO entities (name, phone, size, city, attrs, created_at)
VALUES ('مجمع الرعاية الطبية','966500000850','متوسطة','الرياض',
  '{"size":"متوسطة","city":"الرياض","sector":"مجمعات طبية"}'::jsonb,1786800000000);

-- B. an OLD row from before the props migration: the key is entirely absent (NULL, not '{}').
ALTER TABLE contacts ALTER COLUMN props DROP NOT NULL;
INSERT INTO contacts (phone, wa_name, first_seen_at, last_event_at, status_times, opted_out, human, agent_turns, test, props)
VALUES ('966500000861','مستوصف النور',1786100000000,1786200000000,
  '{"sent":1786100001000,"delivered":1786100002000}'::jsonb,false,false,0,false,NULL);
INSERT INTO messages (phone, role, text, ts) VALUES
 ('966500000861','agent','السلام عليكم، معك مساعد مسار من لين.',1786100300000);

-- C. the contact used for the mid-conversation agent-write scenarios
INSERT INTO contacts (phone, wa_name, first_seen_at, last_event_at, status_times, opted_out, human, agent_turns, test, props)
VALUES ('966500000862','عيادة الشفاء',1786500000000,1786600000000,
  '{"sent":1786500001000,"delivered":1786500002000,"read":1786500050000}'::jsonb,false,false,1,false,'{}'::jsonb);
INSERT INTO messages (phone, role, text, ts) VALUES
 ('966500000862','agent','السلام عليكم، معك مساعد مسار من لين.',1786500300000),
 ('966500000862','customer','عندنا اهتمام بالتطعيمات',1786500400000);
