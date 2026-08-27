# CSV Aliases — 列名兼容

- 归一化：`lower().strip().replace("_"," ")`
- 必选：`Post id/Tweet id`, `Post text/Text`, `Impressions/Views/展示`
- 可选：`Post Link/Permalink`, `Likes`, `Engagements`, `Bookmarks`, `New follows`, `Profile visits`, `Detail Expands`, `URL Clicks`
- 小时不走 `Date`，必须走 Snowflake `(id>>22)+1288834974657` → CST (+8)，校验 `abs(解码日期 - Date) ≤1天`
- 编码 `utf-8-sig`，用 `csv` 模块解析引号/逗号/emoji/t.co
