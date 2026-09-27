# Dead workarounds in 30 popular repos

canidelete found **14334 GitHub issue links and tripwires in code comments**. **11978 of them (84%) point at something that's already resolved**: the issue is closed, the PR merged, or the deadline passed. Not every one is dead code, but every one is a comment worth a second look.

| Repo | Links | ✅ Resolved | 🪦 Won't fix | ⏳ Still needed |
|---|---:|---:|---:|---:|
| [microsoft/TypeScript](https://github.com/microsoft/TypeScript) | 1591 | **1527** | 12 | 44 |
| [oven-sh/bun](https://github.com/oven-sh/bun) | 1579 | **1400** | 103 | 63 |
| [microsoft/vscode](https://github.com/microsoft/vscode) | 1770 | **1268** | 26 | 231 |
| [nodejs/node](https://github.com/nodejs/node) | 1454 | **1079** | 217 | 151 |
| [microsoft/playwright](https://github.com/microsoft/playwright) | 996 | **948** | 15 | 28 |
| [pandas-dev/pandas](https://github.com/pandas-dev/pandas) | 957 | **872** | 15 | 69 |
| [denoland/deno](https://github.com/denoland/deno) | 924 | **791** | 31 | 102 |
| [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) | 810 | **622** | 92 | 89 |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | 561 | **447** | 14 | 100 |
| [eslint/eslint](https://github.com/eslint/eslint) | 448 | **443** | 2 | 1 |
| [prettier/prettier](https://github.com/prettier/prettier) | 480 | **414** | 17 | 49 |
| [huggingface/transformers](https://github.com/huggingface/transformers) | 491 | **366** | 52 | 70 |
| [python/cpython](https://github.com/python/cpython) | 367 | **327** | 11 | 29 |
| [vercel/next.js](https://github.com/vercel/next.js) | 290 | **222** | 18 | 46 |
| [grafana/grafana](https://github.com/grafana/grafana) | 290 | **192** | 17 | 44 |
| [home-assistant/core](https://github.com/home-assistant/core) | 268 | **190** | 15 | 59 |
| [facebook/react](https://github.com/facebook/react) | 197 | **171** | 6 | 17 |
| [tailwindlabs/tailwindcss](https://github.com/tailwindlabs/tailwindcss) | 124 | **123** | 1 | 0 |
| [electron/electron](https://github.com/electron/electron) | 143 | **114** | 23 | 6 |
| [numpy/numpy](https://github.com/numpy/numpy) | 137 | **99** | 7 | 31 |
| [golang/go](https://github.com/golang/go) | 105 | **89** | 4 | 12 |
| [vitejs/vite](https://github.com/vitejs/vite) | 80 | **67** | 4 | 9 |
| [neovim/neovim](https://github.com/neovim/neovim) | 83 | **58** | 5 | 20 |
| [sveltejs/svelte](https://github.com/sveltejs/svelte) | 59 | **41** | 1 | 16 |
| [vuejs/core](https://github.com/vuejs/core) | 40 | **37** | 2 | 1 |
| [rails/rails](https://github.com/rails/rails) | 39 | **28** | 7 | 4 |
| [fastapi/fastapi](https://github.com/fastapi/fastapi) | 20 | **18** | 2 | 0 |
| [django/django](https://github.com/django/django) | 14 | **11** | 2 | 1 |
| [psf/requests](https://github.com/psf/requests) | 14 | **11** | 2 | 1 |
| [pallets/flask](https://github.com/pallets/flask) | 3 | **3** | 0 | 0 |

## Hall of fame: fixed years ago, still worked around

- `facebook/react` [compiler/packages/babel-plugin-react-compiler/src/__tests__/fixtures/compiler/object-keys.js:5](https://github.com/facebook/react/blob/HEAD/compiler/packages/babel-plugin-react-compiler/src/__tests__/fixtures/compiler/object-keys.js#L5) waits on https://github.com/facebook/react/issues/32261, which was closed 13mo ago "[Compiler Bug]: "Ref values (the `current` property) may ..."
- `facebook/react` [compiler/packages/babel-plugin-react-compiler/src/__tests__/fixtures/compiler/object-values.js:5](https://github.com/facebook/react/blob/HEAD/compiler/packages/babel-plugin-react-compiler/src/__tests__/fixtures/compiler/object-values.js#L5) waits on https://github.com/facebook/react/issues/32261, which was closed 13mo ago "[Compiler Bug]: "Ref values (the `current` property) may ..."
- `facebook/react` [compiler/packages/babel-plugin-react-compiler/src/__tests__/fixtures/compiler/repro-object-fromEntries-entries.js:5](https://github.com/facebook/react/blob/HEAD/compiler/packages/babel-plugin-react-compiler/src/__tests__/fixtures/compiler/repro-object-fromEntries-entries.js#L5) waits on https://github.com/facebook/react/issues/32261, which was closed 13mo ago "[Compiler Bug]: "Ref values (the `current` property) may ..."
- `facebook/react` [compiler/packages/snap/src/compiler.ts:150](https://github.com/facebook/react/blob/HEAD/compiler/packages/snap/src/compiler.ts#L150) waits on https://github.com/facebook/fbt/issues/49, which was closed 6y 12mo ago "Typescript support"
- `facebook/react` [fixtures/dom/src/components/fixtures/custom-elements/index.js:17](https://github.com/facebook/react/blob/HEAD/fixtures/dom/src/components/fixtures/custom-elements/index.js#L17) waits on https://github.com/w3c/webcomponents/issues/587, which was closed 9y 11mo ago "Non-class based example of customElement.define()"
- `facebook/react` [fixtures/dom/src/components/fixtures/date-inputs/switch-date-test-case.js:6](https://github.com/facebook/react/blob/HEAD/fixtures/dom/src/components/fixtures/date-inputs/switch-date-test-case.js#L6) waits on https://github.com/facebook/react/issues/8116, which was closed 9y 2mo ago "HTML5 datepicker not updating after type change"
- `facebook/react` [fixtures/dom/src/components/fixtures/hydration/Code.js:15](https://github.com/facebook/react/blob/HEAD/fixtures/dom/src/components/fixtures/hydration/Code.js#L15) waits on https://github.com/graphql/graphiql/issues/33, which was closed 11y 0mo ago "codemirror widths and lefts are so large they push codemi..."
- `facebook/react` [fixtures/dom/src/components/fixtures/hydration/Code.js:61](https://github.com/facebook/react/blob/HEAD/fixtures/dom/src/components/fixtures/hydration/Code.js#L61) waits on https://github.com/facebook/react/issues/13610, which was closed 8y 0mo ago "IE9: Unable to call apply on console.error when encounter..."
- `facebook/react` [fixtures/dom/src/components/fixtures/mouse-events/mouse-enter.js:30](https://github.com/facebook/react/blob/HEAD/fixtures/dom/src/components/fixtures/mouse-events/mouse-enter.js#L30) waits on https://github.com/facebook/react/issues/16763, which was closed 6y 11mo ago "Component sometimes fires event handlers twice"
- `facebook/react` [fixtures/flight/config/env.js:45](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/env.js#L45) waits on https://github.com/facebook/create-react-app/issues/253, which was closed 10y 0mo ago "Respect NODE_PATH environment variable"
- `facebook/react` [fixtures/flight/config/env.js:50](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/env.js#L50) waits on https://github.com/facebook/create-react-app/issues/1023, which was closed 9y 9mo ago "npm run build fails for EventEmitter"
- `facebook/react` [fixtures/flight/config/paths.js:8](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/paths.js#L8) waits on https://github.com/facebook/create-react-app/issues/637, which was closed 10y 0mo ago "Unexpected token (7:2) You may need an appropriate loader..."
- `facebook/react` [fixtures/flight/config/webpack.config.js:122](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/webpack.config.js#L122) waits on https://github.com/facebook/create-react-app/issues/2677, which was closed 9y 3mo ago "Cannot import external CSS files after upgrading to react..."
- `facebook/react` [fixtures/flight/config/webpack.config.js:263](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/webpack.config.js#L263) waits on https://github.com/facebook/create-react-app/issues/2376, which was closed 9y 4mo ago "comparisons compression option in uglifyjs webpack prod c..."
- `facebook/react` [fixtures/flight/config/webpack.config.js:265](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/webpack.config.js#L265) waits on https://github.com/mishoo/UglifyJS2/issues/2011, which was closed 9y 4mo ago "'comparisons' compression option results in incorrect cod..."
- `facebook/react` [fixtures/flight/config/webpack.config.js:268](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/webpack.config.js#L268) waits on https://github.com/facebook/create-react-app/issues/5250, which was closed 7y 12mo ago "Minify Bundle Error in CRA2"
- `facebook/react` [fixtures/flight/config/webpack.config.js:270](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/webpack.config.js#L270) waits on https://github.com/terser-js/terser/issues/120, which was closed 7y 11mo ago "TypeError: Cannot read property '_walk' of null"
- `facebook/react` [fixtures/flight/config/webpack.config.js:283](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/webpack.config.js#L283) waits on https://github.com/facebook/create-react-app/issues/2488, which was closed 9y 3mo ago "Emoji after build"
- `facebook/react` [fixtures/flight/config/webpack.config.js:296](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/webpack.config.js#L296) waits on https://github.com/facebook/create-react-app/issues/253, which was closed 10y 0mo ago "Respect NODE_PATH environment variable"
- `facebook/react` [fixtures/flight/config/webpack.config.js:303](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/webpack.config.js#L303) waits on https://github.com/facebook/create-react-app/issues/290, which was closed 10y 0mo ago "Warn about JSX file extension"
- `facebook/react` [fixtures/flight/config/webpack.config.js:582](https://github.com/facebook/react/blob/HEAD/fixtures/flight/config/webpack.config.js#L582) waits on https://github.com/facebook/create-react-app/issues/240, which was closed 10y 1mo ago "Inconsistent filename casing breaks the watcher"
- `facebook/react` [fixtures/flight/scripts/test.js:46](https://github.com/facebook/react/blob/HEAD/fixtures/flight/scripts/test.js#L46) waits on https://github.com/facebook/create-react-app/issues/5210, which was closed 7y 12mo ago "npm test fails if the project doesn't have git"
- `facebook/react` [fixtures/legacy-jsx-runtimes/react-14/cjs/react-jsx-dev-runtime.development.js:111](https://github.com/facebook/react/blob/HEAD/fixtures/legacy-jsx-runtimes/react-14/cjs/react-jsx-dev-runtime.development.js#L111) waits on https://github.com/facebook/react/issues/13610, which was closed 8y 0mo ago "IE9: Unable to call apply on console.error when encounter..."
- `facebook/react` [fixtures/legacy-jsx-runtimes/react-14/cjs/react-jsx-runtime.development.js:110](https://github.com/facebook/react/blob/HEAD/fixtures/legacy-jsx-runtimes/react-14/cjs/react-jsx-runtime.development.js#L110) waits on https://github.com/facebook/react/issues/13610, which was closed 8y 0mo ago "IE9: Unable to call apply on console.error when encounter..."
- `facebook/react` [fixtures/legacy-jsx-runtimes/react-15/cjs/react-jsx-dev-runtime.development.js:116](https://github.com/facebook/react/blob/HEAD/fixtures/legacy-jsx-runtimes/react-15/cjs/react-jsx-dev-runtime.development.js#L116) waits on https://github.com/facebook/react/issues/13610, which was closed 8y 0mo ago "IE9: Unable to call apply on console.error when encounter..."
