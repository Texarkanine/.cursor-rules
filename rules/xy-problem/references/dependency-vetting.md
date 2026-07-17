# Dependency Vetting

Facts and checks for verifying that a candidate dependency can actually do the job it is being chosen for. This is a reference: consult it during the verification step of a means-decision, in any order.

## Capability Proof

- Locate the exact API for the load-bearing capability in the documentation or source of the version you would install — not in memory, old tutorials, or third-party blog posts.
- Confirm the mechanism, not just the feature name. *How* does it deliver the capability, and at what layer? An HTTP interceptor may monkey-patch `http.request`, register an undici dispatcher, or require routing traffic through a proxy — each catches different traffic, and only one of them may catch yours.
- Check the capability against the project's actual context: runtime and language version, the specific client or framework in use, platform, module system, test runner. A capability that exists in general can still be absent for your combination.
- Read the library's own tests for the capability. They show the supported usage envelope more honestly than the README does.

## Spike Before Building

- Prove the load-bearing capability with the smallest program that exercises it in the project's environment, before writing real code against it.
- The spike must run the actual path — the real client, the real runtime, the real test runner — not the library's happy-path example.
- A spike that needs workarounds to pass is a failed spike. Workarounds at proof time are a mismatch signal; the response is to return to the alternatives survey, not to write adapters.

## Fitness Beyond Capability

- Maintenance: recent releases, and whether open issues cluster on the capability you need.
- Constraints it imports: transitive dependencies, peer requirements, minimum runtime versions, license compatibility.
- Overlap: whether something already installed — or the standard library — covers the goal without a new dependency at all.
