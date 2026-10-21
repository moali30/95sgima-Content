# 95 Sigma Content

المكان اللي بيتجمع فيه شغل المحتوى: الريسرش، خرايط الريلز، البوستات، وصور البوستات والثامبنيلز بهوية 95 Sigma.

## الترتيب

| المسار | فيه إيه |
|---|---|
| `brand/` | الخطوط واللوجوهات وصورة محمد وألوان الديزاين سيستم (منسوخة من 95 Sigma Design System) |
| `templates/card.html` | قالب واحد بيرسم صورة البوست والثامبنيل بكل أشكالهم |
| `render/render.js` | بيحوّل ملف `visual.json` لصور PNG |
| `examples/` | أمثلة جاهزة لكل شكل (`samples.json`) وصورها في `examples/out/` |
| `topics/<تاريخ>-<اسم>/` | ملف لكل موضوع: `research.md`، `reel-map.md` أو `post.md`، `visual.json`، والصور في `out/` |

## تطلع الصور إزاي

```bash
node render/render.js topics/2026-10-25-power-analysis/visual.json
```

الصور بتطلع في `out/` جنب ملف الـ JSON. في جلسات Claude على الويب Playwright متسطب جاهز. على جهازك: `npm install` وبعدين `npx playwright install chromium`.

## المقاسات

| `format` | المقاس | بيستخدم في |
|---|---|---|
| `post` | 1080×1350 | صورة بوست فيسبوك (4:5) |
| `reel` | 1080×1920 | غلاف ريل فيسبوك و YouTube Shorts. الكلام بيفضل بعيد عن أسفل 400px عشان أزرار المنصة |
| `yt` | 1280×720 | ثامبنيل فيديو يوتيوب عادي |

## الأشكال (`variant`)

- `light`: الأساسي للبوستات، خلفية Chalk ورسم إحصائي في كارت أبيض.
- `dark`: خلفية Deep Teal، مناسب لرقم أو معادلة كبيرة.
- `myth`: كارت «الشائع» مشطوب وكارت «الأدق» تحته (للبوست بس).
- `photo`: صورة محمد على Panel فاتح، من غير رسم.

## حقول `visual.json`

الملف ممكن يبقى object واحد أو array. كل عنصر:

| الحقل | إجباري | الوصف |
|---|---|---|
| `name` | لأ | اسم ملف الصورة |
| `format` | أيوه | `post` أو `reel` أو `yt` |
| `variant` | لأ | `light` (الافتراضي) أو `dark` أو `myth` أو `photo` |
| `label` | لأ | تصنيف صغير فوق العنوان، زي «تحليل الانحدار» |
| `series`, `episode` | لأ | اسم السلسلة ورقم الحلقة |
| `title` | أيوه | العنوان. الكلمة اللي بين `*نجمتين*` بتتلوّن بلون الأكسنت |
| `subtitle` | لأ | سطر شرح تحت العنوان |
| `myth.wrong`, `myth.right` | مع `myth` | الجملة الشائعة والجملة الأدق |
| `visual` | لأ | الرسم الإحصائي، شوف تحت |
| `url` | لأ | الافتراضي `95sigma.tech` |

أنواع `visual.type`:

- `number`: رقم أو معادلة كبيرة. `{value, caption}`
- `ci`: نقط بفترات ثقة. `{items:[{label, est, lo, hi, hl}], ref, refLabel, caption}`
- `dist`: توزيعات طبيعية مع منطقة مظللة. `{curves:[{mu, sd, label, hl}], shade:{curve, from, to, label}, cut:{x, label}}`
- `bars`: أعمدة أفقية. `{items:[{label, value, hl}], unit, caption}`
- `dumbbell`: قبل وبعد. `{items:[{label, from, to, hl}], caption}`
- `scatter`: انتشار بمعامل ارتباط. `{r, n, seed, note}`

أي رقم في الرسم لازم يكون من الريسرش أو من محاكاة متوثقة، والـ `caption` بيقول `n` والوحدة. لو المثال توضيحي، الكابشن يقول «مثال توضيحي».
