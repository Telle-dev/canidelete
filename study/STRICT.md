# Workarounds waiting on bugs that are already closed

canidelete found 14334 GitHub issue/PR links in code comments across 30 popular repos. Most of them are just references (a test pointing at the bug it covers, a "see #123" note), so this page only counts comments that **say** they're a workaround or a TODO: words like *workaround*, *hack*, *TODO*, *remove once*, *until*, or a skipped test.

- **258** of those point at an issue that's closed or a PR that's merged
- **207** of them were closed more than a year ago
- **48** more point at issues closed as *not planned* or PRs closed without merging, so the workaround is probably permanent and the comment is misleading

A closed issue doesn't always mean the workaround can go (the fix may be in a version the project doesn't use yet), but every one of these is worth a look.

## Oldest ones

- **kubernetes/kubernetes** [staging/src/k8s.io/apimachinery/pkg/util/naming/from_stack.go:81](https://github.com/kubernetes/kubernetes/blob/HEAD/staging/src/k8s.io/apimachinery/pkg/util/naming/from_stack.go#L81): closed 11y 2mo ago "runtime: A new method to get function created goroutine r..."  
  `// TODO: Go does not expose this via runtime https://github.com/golang/go/issues/11440`
- **kubernetes/kubernetes** [test/e2e/common/storage/downwardapi_volume.go:531](https://github.com/kubernetes/kubernetes/blob/HEAD/test/e2e/common/storage/downwardapi_volume.go#L531): PR merged 11y 0mo ago "downward api volume plugin"  
  `// TODO: add test-webserver example as pointed out in https://github.com/kubernetes/kubernetes/pull/5093#discussion-diff-37606771`
- **kubernetes/kubernetes** [pkg/kubelet/kubelet_node_status_test.go:340](https://github.com/kubernetes/kubernetes/blob/HEAD/pkg/kubelet/kubelet_node_status_test.go#L340): closed 10y 10mo ago "Unable to schedule pods in mixed version cluster (schedul..."  
  `// Version skew workaround. See: https://github.com/kubernetes/kubernetes/issues/16961`
- **kubernetes/kubernetes** [pkg/kubelet/kubelet_node_status_test.go:537](https://github.com/kubernetes/kubernetes/blob/HEAD/pkg/kubelet/kubelet_node_status_test.go#L537): closed 10y 10mo ago "Unable to schedule pods in mixed version cluster (schedul..."  
  `// Version skew workaround. See: https://github.com/kubernetes/kubernetes/issues/16961`
- **kubernetes/kubernetes** [pkg/kubelet/kubelet_node_status_test.go:739](https://github.com/kubernetes/kubernetes/blob/HEAD/pkg/kubelet/kubelet_node_status_test.go#L739): closed 10y 10mo ago "Unable to schedule pods in mixed version cluster (schedul..."  
  `// Version skew workaround. See: https://github.com/kubernetes/kubernetes/issues/16961`
- **kubernetes/kubernetes** [pkg/kubelet/kubelet_node_status_test.go:976](https://github.com/kubernetes/kubernetes/blob/HEAD/pkg/kubelet/kubelet_node_status_test.go#L976): closed 10y 10mo ago "Unable to schedule pods in mixed version cluster (schedul..."  
  `// Version skew workaround. See: https://github.com/kubernetes/kubernetes/issues/16961`
- **microsoft/vscode** [extensions/typescript-language-features/src/languageFeatures/formatting.ts:70](https://github.com/microsoft/vscode/blob/HEAD/extensions/typescript-language-features/src/languageFeatures/formatting.ts#L70): closed 10y 4mo ago "formatOnType does not respect current line indendtiation"  
  `// Work around for https://github.com/microsoft/TypeScript/issues/6700.`
- **microsoft/vscode** [src/vs/workbench/contrib/webview/browser/pre/index.html:1104](https://github.com/microsoft/vscode/blob/HEAD/src/vs/workbench/contrib/webview/browser/pre/index.html#L1104): closed 10y 0mo ago "Markdown preview: some files flicker/reset scroll positio..."  
  `// Workaround for https://github.com/microsoft/vscode/issues/12865`
- **microsoft/vscode** [src/vs/editor/browser/services/openerService.ts:87](https://github.com/microsoft/vscode/blob/HEAD/src/vs/editor/browser/services/openerService.ts#L87): closed 9y 11mo ago "HTML mode produces non-normalized links"  
  `target = normalizePath(target); // workaround for non-normalized paths (https://github.com/microsoft/vscode/issues/12954)`
- **microsoft/vscode** [src/vs/platform/configuration/common/configuration.ts:276](https://github.com/microsoft/vscode/blob/HEAD/src/vs/platform/configuration/common/configuration.ts#L276): closed 9y 11mo ago "Fails to start when settings contain the same key prefix ..."  
  `(curr as IStringDictionary<unknown>)[last] = value; // workaround https://github.com/microsoft/vscode/issues/13606`
- **nodejs/node** [test/fixtures/wpt/webidl/current-realm.html:4](https://github.com/nodejs/node/blob/HEAD/test/fixtures/wpt/webidl/current-realm.html#L4): closed 9y 11mo ago "Bug 29514 - Need to define which globals objects created ..."  
  `TODO: https://github.com/w3c/webcrypto/issues/85 -->`
- **microsoft/vscode** [src/server-main.ts:384](https://github.com/microsoft/vscode/blob/HEAD/src/server-main.ts#L384): closed 9y 6mo ago ""Implement me. Unknown stdin file type!" error thrown whe..."  
  `// Windows workaround for https://github.com/nodejs/node/issues/11656`
- **microsoft/vscode** [src/vs/platform/environment/node/stdin.ts:16](https://github.com/microsoft/vscode/blob/HEAD/src/vs/platform/environment/node/stdin.ts#L16): closed 9y 6mo ago ""Implement me. Unknown stdin file type!" error thrown whe..."  
  `// Windows workaround for https://github.com/nodejs/node/issues/11656`
- **kubernetes/kubernetes** [staging/src/k8s.io/apiserver/pkg/server/genericapiserver.go:80](https://github.com/kubernetes/kubernetes/blob/HEAD/staging/src/k8s.io/apiserver/pkg/server/genericapiserver.go#L80): closed 9y 4mo ago "Remove the concept of "unversioned" types and replace it ..."  
  `// TODO: Remove this when https://github.com/kubernetes/kubernetes/issues/19018 is fixed.`
- **nodejs/node** [test/parallel/test-child-process-fork-getconnections.js:46](https://github.com/nodejs/node/blob/HEAD/test/parallel/test-child-process-fork-getconnections.js#L46): closed 9y 2mo ago "intermittent unexpected socket closure on Mac OS X"  
  `// Workaround for https://github.com/nodejs/node/issues/2610`
- **microsoft/vscode** [extensions/typescript-language-features/src/languageFeatures/completions.ts:281](https://github.com/microsoft/vscode/blob/HEAD/extensions/typescript-language-features/src/languageFeatures/completions.ts#L281): closed 8y 12mo ago "`completionEntryDetails` Should Not Return Parameters In ..."  
  `// Workaround for https://github.com/microsoft/TypeScript/issues/12677`
- **denoland/deno** [libs/eszip/testdata/dotland.json:125](https://github.com/denoland/deno/blob/HEAD/libs/eszip/testdata/dotland.json#L125): closed 8y 10mo ago "Extending Promise gives runtime error: undefined is not a..."  
  `"source": "// Copyright 2018-2021 the Deno authors. All rights reserved. MIT license.\n// TODO(ry) It'd be better to make Deferred a class that inherits from\n/`
- **denoland/deno** [libs/eszip/testdata/dotland.json:208](https://github.com/denoland/deno/blob/HEAD/libs/eszip/testdata/dotland.json#L208): closed 8y 10mo ago "Extending Promise gives runtime error: undefined is not a..."  
  `"source": "// Copyright 2018-2021 the Deno authors. All rights reserved. MIT license.\n// TODO(ry) It'd be better to make Deferred a class that inherits from\n/`
- **oven-sh/bun** [test/cli/install/registry/verdaccio.yaml:113](https://github.com/oven-sh/bun/blob/HEAD/test/cli/install/registry/verdaccio.yaml#L113): closed 8y 10mo ago "Unexpected EOF while installing/downloading large packages"  
  `# WORKAROUND: Through given configuration you can workaround following issue https://github.com/verdaccio/verdaccio/issues/301. Set to 0 in case 60 is not enoug`
- **grafana/grafana** [devenv/local-npm/conf/config.yaml:108](https://github.com/grafana/grafana/blob/HEAD/devenv/local-npm/conf/config.yaml#L108): closed 8y 10mo ago "Unexpected EOF while installing/downloading large packages"  
  `# WORKAROUND: Through given configuration you can workaround following issue https://github.com/verdaccio/verdaccio/issues/301. Set to 0 in case 60 is not enoug`
- **microsoft/vscode** [src/vs/base/browser/markdownRenderer.ts:124](https://github.com/microsoft/vscode/blob/HEAD/src/vs/base/browser/markdownRenderer.ts#L124): closed 8y 9mo ago "Does not Handle Markdown Escapes In Link Href"  
  `// Remove markdown escapes. Workaround for https://github.com/chjj/marked/issues/829`
- **microsoft/vscode** [src/vs/workbench/contrib/tasks/common/problemCollectors.ts:418](https://github.com/microsoft/vscode/blob/HEAD/src/vs/workbench/contrib/tasks/common/problemCollectors.ts#L418): closed 8y 7mo ago "building never ends"  
  `// workaround for https://github.com/microsoft/vscode/issues/44018`
- **kubernetes/kubernetes** [pkg/controller/namespace/deletion/namespaced_resources_deleter.go:330](https://github.com/kubernetes/kubernetes/blob/HEAD/pkg/controller/namespace/deletion/namespaced_resources_deleter.go#L330): closed 8y 7mo ago "Confusing results from discovery client confuses namespac..."  
  `// TODO: https://github.com/kubernetes/kubernetes/issues/22413`
- **kubernetes/kubernetes** [pkg/controller/namespace/deletion/namespaced_resources_deleter.go:365](https://github.com/kubernetes/kubernetes/blob/HEAD/pkg/controller/namespace/deletion/namespaced_resources_deleter.go#L365): closed 8y 7mo ago "Confusing results from discovery client confuses namespac..."  
  `// TODO: https://github.com/kubernetes/kubernetes/issues/22413`
- **kubernetes/kubernetes** [test/e2e/common/node/kubelet_etc_hosts.go:107](https://github.com/kubernetes/kubernetes/blob/HEAD/test/e2e/common/node/kubelet_etc_hosts.go#L107): closed 8y 7mo ago ""kubectl exec" sometimes incorrectly returns empty string..."  
  `// TODO: workaround for https://github.com/kubernetes/kubernetes/issues/34256`
- **kubernetes/kubernetes** [pkg/kubelet/kuberuntime/kuberuntime_manager.go:303](https://github.com/kubernetes/kubernetes/blob/HEAD/pkg/kubelet/kuberuntime/kuberuntime_manager.go#L303): closed 8y 4mo ago "kubelet container runtime API machinery"  
  `// TODO: Runtime API machinery is under discussion at https://github.com/kubernetes/kubernetes/issues/28642`
- **microsoft/vscode** [src/vs/base/node/processes.ts:36](https://github.com/microsoft/vscode/blob/HEAD/src/vs/base/node/processes.ts#L36): closed 8y 3mo ago "IPC can freeze the process"  
  `// to workaround https://github.com/nodejs/node/issues/7657 (IPC can freeze process)`
- **microsoft/vscode** [src/vs/base/node/processes.ts:62](https://github.com/microsoft/vscode/blob/HEAD/src/vs/base/node/processes.ts#L62): closed 8y 3mo ago "IPC can freeze the process"  
  `if (!result \|\| Platform.isWindows /* workaround https://github.com/nodejs/node/issues/7657 */) {`
- **microsoft/vscode** [src/vs/workbench/contrib/webview/browser/webviewElement.ts:732](https://github.com/microsoft/vscode/blob/HEAD/src/vs/workbench/contrib/webview/browser/webviewElement.ts#L732): closed 8y 1mo ago "Webview: traps keyboard events once focused"  
  `// Electron: workaround for https://github.com/electron/electron/issues/14258`
- **microsoft/TypeScript** [tsc/testdata/tests/cases/compiler/arrayConcat3.ts:3](https://github.com/microsoft/TypeScript/blob/HEAD/tsc/testdata/tests/cases/compiler/arrayConcat3.ts#L3): closed 8y 1mo ago "Array of generic functions not assignable to ReadonlyArray"  
  `// TODO: remove lib hack when https://github.com/Microsoft/TypeScript/issues/20454 is fixed`
- **microsoft/vscode** [src/vs/platform/windows/electron-main/windowImpl.ts:1037](https://github.com/microsoft/vscode/blob/HEAD/src/vs/platform/windows/electron-main/windowImpl.ts#L1037): closed 8y 0mo ago "[mitigated] Electron 3.0.x: pausing in devtools can trigg..."  
  `// TODO@electron Workaround for https://github.com/microsoft/vscode/issues/56994`
- **microsoft/vscode** [src/vs/workbench/contrib/search/browser/replaceService.ts:84](https://github.com/microsoft/vscode/blob/HEAD/src/vs/workbench/contrib/search/browser/replaceService.ts#L84): closed 8y 0mo ago "Continue further adoption of ITextModelResolverService"  
  `this._register(fileMatch.onDispose(() => replacePreviewModel.dispose())); // TODO@Sandeep we should not dispose a model directly but rather the reference (depen`
- **nodejs/node** [tools/v8_gypfiles/toolchain.gypi:753](https://github.com/nodejs/node/blob/HEAD/tools/v8_gypfiles/toolchain.gypi#L753): PR merged 7y 11mo ago "deps: fix wrong default for v8 handle zapping"  
  `# Temporary refs: https://github.com/nodejs/node/pull/23801`
- **nodejs/node** [tools/v8_gypfiles/toolchain.gypi:767](https://github.com/nodejs/node/blob/HEAD/tools/v8_gypfiles/toolchain.gypi#L767): PR merged 7y 11mo ago "deps: fix wrong default for v8 handle zapping"  
  `# Temporary refs: https://github.com/nodejs/node/pull/23801`
- **vercel/next.js** [test/production/pages-dir/production/test/index.test.ts:992](https://github.com/vercel/next.js/blob/HEAD/test/production/pages-dir/production/test/index.test.ts#L992): closed 7y 7mo ago "Safari cache on dev"  
  `// This is a workaround to fix https://github.com/vercel/next.js/issues/5860`
- **vercel/next.js** [turbopack/crates/turbopack-tracing/tests/node-file-trace/test/unit/webpack-wrapper-strs-namespaces-large/input.js:3295](https://github.com/vercel/next.js/blob/HEAD/turbopack/crates/turbopack-tracing/tests/node-file-trace/test/unit/webpack-wrapper-strs-namespaces-large/input.js#L3295): closed 7y 7mo ago "Safari cache on dev"  
  `// This is a workaround to fix https://github.com/vercel/next.js/issues/5860`
- **oven-sh/bun** [packages/bun-usockets/src/crypto/default_ciphers.h:26](https://github.com/oven-sh/bun/blob/HEAD/packages/bun-usockets/src/crypto/default_ciphers.h#L26): closed 7y 7mo ago "Support BoringSSL as alternative to OpenSSL"  
  `// In node.js they filter TLS_* ciphers and use SSL_CTX_set_cipher_list (TODO: Electron has a patch https://github.com/nodejs/node/issues/25890)`
- **golang/go** [lib/wasm/wasm_exec.js:288](https://github.com/golang/go/blob/HEAD/lib/wasm/wasm_exec.js#L288): closed 7y 6mo ago "all: tests deadlocked on js/wasm"  
  `// (temporary workaround for https://github.com/golang/go/issues/28975)`
- **microsoft/vscode** [src/vs/base/parts/contextmenu/electron-main/contextmenu.ts:19](https://github.com/microsoft/vscode/blob/HEAD/src/vs/base/parts/contextmenu/electron-main/contextmenu.ts#L19): closed 7y 5mo ago "Right Click Menu Closing Without User Input"  
  `// Workaround for https://github.com/microsoft/vscode/issues/72447`
- **nodejs/node** [deps/v8/test/mjsunit/harmony/promise-all-settled.js:166](https://github.com/nodejs/node/blob/HEAD/deps/v8/test/mjsunit/harmony/promise-all-settled.js#L166): PR merged 7y 5mo ago "Optimize constructor.resolve lookup"  
  `// TODO(mathias): https://github.com/tc39/proposal-promise-allSettled/pull/40`

## Per repo

| Repo | Workaround comments on resolved issues |
|---|---:|
| [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) | 63 |
| [microsoft/vscode](https://github.com/microsoft/vscode) | 59 |
| [grafana/grafana](https://github.com/grafana/grafana) | 29 |
| [huggingface/transformers](https://github.com/huggingface/transformers) | 28 |
| [microsoft/playwright](https://github.com/microsoft/playwright) | 24 |
| [denoland/deno](https://github.com/denoland/deno) | 17 |
| [oven-sh/bun](https://github.com/oven-sh/bun) | 17 |
| [pandas-dev/pandas](https://github.com/pandas-dev/pandas) | 17 |
| [nodejs/node](https://github.com/nodejs/node) | 15 |
| [vercel/next.js](https://github.com/vercel/next.js) | 5 |
| [neovim/neovim](https://github.com/neovim/neovim) | 5 |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | 4 |
| [microsoft/TypeScript](https://github.com/microsoft/TypeScript) | 3 |
| [electron/electron](https://github.com/electron/electron) | 3 |
| [prettier/prettier](https://github.com/prettier/prettier) | 3 |
| [python/cpython](https://github.com/python/cpython) | 3 |
| [numpy/numpy](https://github.com/numpy/numpy) | 2 |
| [home-assistant/core](https://github.com/home-assistant/core) | 2 |
| [golang/go](https://github.com/golang/go) | 2 |
| [facebook/react](https://github.com/facebook/react) | 1 |
| [sveltejs/svelte](https://github.com/sveltejs/svelte) | 1 |
| [fastapi/fastapi](https://github.com/fastapi/fastapi) | 1 |
| [vitejs/vite](https://github.com/vitejs/vite) | 1 |
| [eslint/eslint](https://github.com/eslint/eslint) | 1 |
