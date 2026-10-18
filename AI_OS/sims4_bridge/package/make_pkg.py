"""Builds GProjectAskBrain.package: two pie-menu interactions + strings (run with plain python3)."""
import struct, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dbpf.py')) else '.')
import dbpf

S = {
    "GP_ASK_NAME": "Ask the AI...", "GP_ASK_TEXT": "What should the AI do?", "GP_ASK_HINT": "Type your request",
    "GP_RATE_NAME": "Rate last AI task...", "GP_RATE_TEXT": "Score the last finished task from 0 (bad) to 5 (great). Leave a box empty to skip it.",
    "GP_TITLE": "G-Project AI OS",
    "GP_Q": "Quality 0-5", "GP_A": "Accuracy 0-5", "GP_S": "Speed 0-5", "GP_SP": "Followed spec 0-5", "GP_C": "Creativity 0-5",
}
K = {k: dbpf.fnv32(k) for k in S}
h = lambda k: "0x%08X" % K[k]


def tuning(name, cls, display, text, inputs):
    iid = dbpf.fnv64(name)
    ins = "".join('      <U n="%s">\n        <V n="default_text" t="enabled"><T n="enabled">%s</T></V>\n      </U>\n' % (n, h(k)) for n, k in inputs)
    xml = '''<?xml version="1.0" encoding="utf-8"?>
<I c="%s" i="interaction" m="gproject_bridge.ask_interaction" n="%s" s="%d">
  <V n="_saveable" t="disabled" />
  <T n="attention_cost">0</T>
  <V n="content_score" t="disabled" />
  <U n="dialog">
    <V n="text" t="single"><T n="single">%s</T></V>
    <U n="text_inputs">
%s    </U>
    <V n="title" t="enabled"><T n="enabled">%s</T></V>
  </U>
  <T n="display_name">%s</T>
  <L n="interaction_category_tags">
    <E>Interaction_Super</E>
    <E>Interaction_All</E>
  </L>
  <E n="scoring_priority">NORMAL</E>
  <T n="time_overhead">0</T>
</I>
''' % (cls, name, iid, h(text), ins, h("GP_TITLE"), h(display))
    return iid, xml


a_id, a_xml = tuning("GProject_AskBrain", "AskBrainInteraction", "GP_ASK_NAME", "GP_ASK_TEXT", [("prompt", "GP_ASK_HINT")])
r_id, r_xml = tuning("GProject_RateTask", "RateTaskInteraction", "GP_RATE_NAME", "GP_RATE_TEXT",
                     [("quality", "GP_Q"), ("accuracy", "GP_A"), ("speed", "GP_S"), ("spec", "GP_SP"), ("creativity", "GP_C")])
ent = b""
for k, v in S.items():
    b = v.encode("utf-8")
    ent += struct.pack("<IBH", K[k], 0, len(b)) + b
stbl = b"STBL" + struct.pack("<HBQHI", 5, 0, len(S), 0, len(ent)) + ent
sid = dbpf.fnv64("GProject_AskBrain_Strings") & 0x00FFFFFFFFFFFFFF
out = sys.argv[1] if len(sys.argv) > 1 else "GProjectAskBrain.package"
dbpf.write_package(out, [(0xE882D22F, 0, a_id, a_xml.encode()), (0xE882D22F, 0, r_id, r_xml.encode()), (0x220557DA, 0, sid, stbl)])
open(os.path.splitext(out)[0] + "_AskBrain.xml", "w").write(a_xml)
open(os.path.splitext(out)[0] + "_RateTask.xml", "w").write(r_xml)
print("ok", hex(a_id), hex(r_id))
