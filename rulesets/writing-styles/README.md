# Writing Styles Ruleset

Short decompression keys for prose writing styles. This ruleset ships only the manual directives as Skills that the agent cannot choose to invoke.

The always-on `always-respond-*` and `always-write-*` rules live a la carte under `rules/` and are **not** in this ruleset — install one of those if **and only if** you want the style on every reply or every prose write.

## The Styles

- **ASD-STE100** — [Simplified Technical English](https://www.asd-ste100.org/).
- **ISO 24495** — [Plain language: relevant, findable, understandable, usable](https://www.iplfederation.org/iso-standard/).
- **TTT** — Classical style as [Steven Pinker](https://en.wikipedia.org/wiki/Steven_Pinker) describes it, per Thomas and Turner's book [*Clear and Simple as the Truth*](https://press.princeton.edu/books/hardcover/9780691654744/clear-and-simple-as-the-truth).
- **Orwell 6** — [George Orwell's six rules for writing]().

## Skills

These skills are *not* invokable by the agent. Invoke them yourself, command-style, when you want one of the writing styles applied to a task.

1. ✈️ [asd-ste100-style](../../rules/asd-ste100-style/SKILL.md)
2. 📄 [iso-24495-style](../../rules/iso-24495-style/SKILL.md)
3. ✒️ [thomas-turner-truth-style](../../rules/thomas-turner-truth-style/SKILL.md)
4. 📰 [orwell-6-style](../../rules/orwell-6-style/SKILL.md)

## Rules

These rules are *not* included in this ruleset - but you might be interested. Mix and match them per your preferences and use-cases to tune your agent's default response and writing styles independently:

### Response Rules

Change how your agent responds to you:

1. ✈️ [always-respond-asd-ste100.mdc](../../rules/always-respond-asd-ste100.mdc)
2. 📄 [always-respond-iso-24495.mdc](../../rules/always-respond-iso-24495.mdc)
3. ✒️ [always-respond-thomas-turner-truth.mdc](../../rules/always-respond-thomas-turner-truth.mdc)
4. 📰 [always-respond-orwell-6.mdc](../../rules/always-respond-orwell-6.mdc)

### Authorship Rules

Change how your agent writes prose, including documents and code comments, etc:

1. ✈️ [always-write-asd-ste100.mdc](../../rules/always-write-asd-ste100.mdc)
2. 📄 [always-write-iso-24495.mdc](../../rules/always-write-iso-24495.mdc)
3. ✒️ [always-write-thomas-turner-truth.mdc](../../rules/always-write-thomas-turner-truth.mdc)
4. 📰 [always-write-orwell-6.mdc](../../rules/always-write-orwell-6.mdc)

## Sample

Shared prompt:

> Explain what NodeJS is.


| Style | Claude Opus 5 |
| --- | --- |
| (no guidance) | Node.js is a runtime that lets JavaScript run outside a web browser — most commonly on servers, but also for command-line tools, build scripts, and desktop apps.<br><br>**The core idea**<br><br>JavaScript was originally confined to the browser. Node.js takes V8 (Chrome's JavaScript engine) and bundles it with APIs the browser doesn't provide: file system access, networking, processes, and OS-level operations. The result is a general-purpose programming platform that happens to use JavaScript as its language.<br><br>... |
| ASD-STE100 | Node.js is a runtime that runs JavaScript outside a web browser.<br><br>Before Node.js, JavaScript ran only inside browser pages. Node.js takes Google's V8 JavaScript engine (the engine from Chrome) and adds libraries for tasks that a browser does not permit: read and write files, open network sockets, start processes, and talk to databases. Thus you can write servers, command-line tools, and build scripts in JavaScript.<br><br>... |
| ISO 24495 | Node.js is a program that runs JavaScript code outside a web browser. Before it existed, JavaScript ran only inside browser pages. Node.js took Google Chrome's JavaScript engine (V8), wrapped it in a standalone runtime, and gave it access to things browsers deliberately withhold: files, network sockets, and the operating system.<br><br>So Node.js is a **runtime**, not a language and not a framework.<br><br>... |
| TTT | Node.js is a program that runs JavaScript outside a web browser.<br><br>That sentence carries most of the story, but the history explains why it matters. JavaScript was invented to make web pages react to clicks and typing, and for its first decade it lived only inside the browser. In 2009 Ryan Dahl took Google's V8 engine — the fast JavaScript interpreter built for Chrome — pulled it out of the browser, and wrapped it in a runtime that could open files, listen on network sockets, and talk to a database. Suddenly the language of the front end could also write the back end.<br><br>... |
| Orwell 6 | Node.js is a program that runs JavaScript outside a web browser.<br><br>JavaScript began as a language for making web pages interactive, and for years it only ran inside browsers. In 2009 Ryan Dahl took Google Chrome's JavaScript engine, V8, and wrapped it in a runtime that could open files, listen on network sockets, and talk to databases. That runtime is Node.js. It let people write servers, command-line tools, and build scripts in the same language they already used for the front end.<br><br>... |

Full responses:

<details><summary>(No Guidance)</summary>


Node.js is a runtime that lets JavaScript run outside a web browser — most commonly on servers, but also for command-line tools, build scripts, and desktop apps.

**The core idea**

JavaScript was originally confined to the browser. Node.js takes V8 (Chrome's JavaScript engine) and bundles it with APIs the browser doesn't provide: file system access, networking, processes, and OS-level operations. The result is a general-purpose programming platform that happens to use JavaScript as its language.

**How it executes code**

Node is single-threaded for your JavaScript, and it's built around non-blocking I/O with an event loop. When your code asks to read a file or make a network request, Node hands the work off and immediately moves on to whatever's next; when the I/O finishes, a callback (or a resolved promise) gets queued to run. This is why Node handles many concurrent connections cheaply — a few thousand open sockets that are mostly idle cost very little, since there's no thread sitting blocked on each one.

The tradeoff: CPU-heavy work (image processing, big cryptographic loops, heavy parsing) blocks that single thread and stalls everything else. Node offers `worker_threads` and child processes for those cases, but the design clearly favors I/O-bound workloads.

**The ecosystem**

Node ships with npm, the package manager, backed by the largest public package registry in existence. A `package.json` file declares your dependencies and scripts. This ecosystem is a genuine strength — there's a library for nearly everything — and a genuine liability, since dependency trees get deep and supply-chain security matters.

**What it's typically used for**

- REST and GraphQL APIs (Express, Fastify, NestJS)
- Full-stack web frameworks (Next.js, Remix, SvelteKit)
- CLI tools — Claude Code itself runs on Node
- Build tooling (bundlers, transpilers, test runners)
- Real-time services over WebSockets
- Desktop apps via Electron

**Practical notes**

Modern Node supports both module systems: CommonJS (`require`) and ES modules (`import`). New projects generally use ES modules. Releases come in even-numbered LTS lines that get long-term support, and odd-numbered lines that don't — use LTS for anything you care about. Version management is usually handled with `nvm`, `fnm`, or Volta.

Alternatives worth knowing: **Deno** (same creator, security-by-default, TypeScript built in) and **Bun** (a fast, Node-compatible runtime with a bundled toolchain). Node remains the default choice for production work, largely on ecosystem maturity and stability.
</details>

<details><summary>ASD-STE100</summary>


## Node.js

Node.js is a runtime that runs JavaScript outside a web browser.

Before Node.js, JavaScript ran only inside browser pages. Node.js takes Google's V8 JavaScript engine (the engine from Chrome) and adds libraries for tasks that a browser does not permit: read and write files, open network sockets, start processes, and talk to databases. Thus you can write servers, command-line tools, and build scripts in JavaScript.

### Key properties

**One thread, non-blocking I/O.** Your code runs on a single thread. When the code starts a slow operation (a disk read, a network call), Node.js does not wait. It registers a callback, continues with other work, and runs the callback when the data is ready. An internal loop, the *event loop*, controls this cycle. Because of this design, one Node.js process can hold many thousands of open connections with little memory.

The limit: if your code does long calculations, it blocks the thread and stops all other work. Node.js is a good fit for I/O-heavy work, less so for CPU-heavy work. For CPU-heavy work, use worker threads or a different language.

**npm.** Node.js includes npm, the package manager. The npm registry is the largest software registry in the world. You declare dependencies in a `package.json` file, and npm installs them.

**Same language on both sides.** The browser and the server use JavaScript. You can share validation rules, types, and utility code between them.

### Typical uses

- HTTP APIs and web servers (Express, Fastify, NestJS)
- Server-side rendering for React, Vue, and Svelte (Next.js, Nuxt)
- Command-line tools
- Build tools and bundlers (Vite, webpack, esbuild)
- Desktop applications, through Electron

### A minimal example

```javascript
import { createServer } from 'node:http';

createServer((req, res) => {
  res.end('Hello from Node.js\n');
}).listen(3000);
```

Save this as `server.js`, then run `node server.js`.

### Related items

- **Deno** and **Bun** are newer runtimes with the same purpose. Bun is faster in many tests and is mostly compatible with Node.js.
- **TypeScript** adds static types to JavaScript. Recent Node.js versions run TypeScript files directly.
- Releases with an even version number become **LTS** (Long Term Support). Use an LTS version for production systems.
</details>

<details><summary>ISO 24495</summary>


## Node.js in short

Node.js is a program that runs JavaScript code outside a web browser. Before it existed, JavaScript ran only inside browser pages. Node.js took Google Chrome's JavaScript engine (V8), wrapped it in a standalone runtime, and gave it access to things browsers deliberately withhold: files, network sockets, and the operating system.

So Node.js is a **runtime**, not a language and not a framework.

## What it's used for

- **Web servers and APIs** — the most common use. Frameworks like Express, Fastify, and Next.js run on it.
- **Build tools** — bundlers, linters, and test runners for front-end projects are usually Node programs.
- **Command-line tools** — including Claude Code itself.
- **Scripts and automation** — file processing, data tasks, glue code.

## How it works

Node.js runs your code on a single main thread and handles waiting differently from most traditional server platforms. When your code asks for something slow — a database query, a file read, an HTTP call — Node hands the work off, moves on to other requests, and comes back when a result arrives. This is called **non-blocking, event-driven I/O**.

The practical effect: one Node process can hold thousands of open connections at once, because waiting costs almost nothing. The tradeoff: heavy computation on the main thread blocks everything else, so Node suits I/O-heavy work (serving requests) better than CPU-heavy work (video encoding, large simulations). For CPU-heavy tasks, Node offers worker threads.

## The ecosystem

Node ships with **npm**, a package manager and public registry with over two million packages. You install a dependency with `npm install <name>`; your project's dependencies and scripts live in a `package.json` file. Alternative package managers — pnpm, Yarn, Bun — read the same format.

## Related things people confuse it with

| Name | What it is |
|---|---|
| **npm** | Node's package manager, bundled with it |
| **Deno**, **Bun** | Competing JavaScript runtimes with similar goals |
| **Express**, **Next.js** | Frameworks that run *on* Node |
| **V8** | The JavaScript engine inside Node |

## Practical notes

Node.js is open source, maintained under the OpenJS Foundation, and runs on Linux, macOS, and Windows. Releases alternate: even-numbered versions get long-term support (LTS) and are the safe choice for production; odd-numbered ones are shorter-lived. Most teams manage versions with a tool like `nvm` or `fnm` so different projects can use different Node versions.
</details>

<details><summary>Thomas and Turner's Truth</summary>


Node.js is a program that runs JavaScript outside a web browser.

That sentence carries most of the story, but the history explains why it matters. JavaScript was invented to make web pages react to clicks and typing, and for its first decade it lived only inside the browser. In 2009 Ryan Dahl took Google's V8 engine — the fast JavaScript interpreter built for Chrome — pulled it out of the browser, and wrapped it in a runtime that could open files, listen on network sockets, and talk to a database. Suddenly the language of the front end could also write the back end.

The second idea in Node is how it handles waiting. A server spends most of its life waiting: for a disk to return a file, for a database to answer, for a slow client to finish sending a request. Many older servers handle this by dedicating a thread to each connection, and each thread costs memory whether it is working or idle. Node instead runs your code on a single thread and never blocks it. When you ask for a file, you hand Node a function to call once the file arrives, and Node moves on to other work. An internal loop — the event loop — watches for finished operations and calls your functions back as results come in. One thread can therefore juggle thousands of connections, provided none of them monopolizes it with heavy computation. That caveat is real: a long number-crunching loop stalls everything, which is why Node suits I/O-heavy work like APIs and proxies better than it suits video encoding.

Modern Node writes this waiting with `async` and `await` rather than nested callbacks, so the code reads top to bottom even though it doesn't execute that way.

Around the runtime grew npm, the package registry, which is arguably as important as Node itself. It holds well over two million packages, and its conventions made sharing small libraries almost frictionless. That abundance is a mixed blessing — a modest project can pull in hundreds of transitive dependencies — but it is why so much of the world's tooling, including bundlers, linters, and test runners, is written for Node even by teams whose applications are not.

What people build with it: web servers and JSON APIs, command-line tools, build systems, real-time services like chat and collaborative editing, and the development tooling underneath most front-end frameworks.

Two clarifications worth keeping straight. Node is a runtime, not a framework — Express, Fastify, and NestJS are frameworks that run on it. And it has competitors now that share its basic bargain: Deno, from the same author, and Bun, which is faster at startup and bundles its own toolchain. Node remains the default, largely because the ecosystem is there.
</details>

<details><summary>Orwell's 6</summary>


Node.js is a program that runs JavaScript outside a web browser.

JavaScript began as a language for making web pages interactive, and for years it only ran inside browsers. In 2009 Ryan Dahl took Google Chrome's JavaScript engine, V8, and wrapped it in a runtime that could open files, listen on network sockets, and talk to databases. That runtime is Node.js. It let people write servers, command-line tools, and build scripts in the same language they already used for the front end.

**How it works.** Node runs your code on a single thread and never waits idly. When you ask it to read a file or fetch a URL, it hands the job to the operating system and moves on to the next task; when the job finishes, Node calls back into your code. This is the "event loop." The design suits work that spends most of its time waiting on the network — web APIs, proxies, chat servers — because one Node process can juggle thousands of open connections. It suits heavy number-crunching far less, since a long calculation blocks everything else. (Node does offer worker threads for that case.)

**What comes with it.** A standard library for files, HTTP, crypto, and streams. A package manager, npm, whose registry holds several million libraries — the largest such collection anywhere, and a mixed blessing: you rarely write anything from scratch, but you inherit other people's code and their bugs.

**What people build with it.** Web backends (Express, Fastify, NestJS), the tooling behind nearly every front-end project (bundlers, test runners, linters), desktop apps through Electron, and small scripts that would once have been shell or Python.

**The neighbors.** Deno and Bun are newer runtimes that do the same job with different trade-offs. Node remains the default.
</details>
