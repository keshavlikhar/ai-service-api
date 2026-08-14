# AI Service API Quiz Answer Key

Use this key to check reasoning, not to memorize wording. Equivalent answers
are valid when they identify the correct responsibility and tradeoff.

## A. Foundations and architecture

1. **Uvicorn.** It is the ASGI server accepting connections and invoking the
   FastAPI application.
2. Keeping domain logic in a service avoids coupling it to HTTP and makes it
   reusable and directly testable.
3. They mark directories as Python packages. They may also define a package's
   public imports, but this project intentionally leaves most of them empty.
4. Uvicorn needs an importable application object, while `create_app()` remains
   available to create isolated, configurable instances.
5. One valid sequence is: client -> Uvicorn -> request-ID middleware -> FastAPI
   router -> Pydantic request validation -> route -> prompt service -> Pydantic
   response -> middleware response header -> client.
6. The schema/API boundary should reject malformed prompt input before business
   logic runs.
7. The prompt service should calculate the word count.
8. It would reverse the intended dependency direction and couple domain logic
   to the HTTP framework.

## B. Python, validation, and testing

9. `pyproject.toml` declares direct requirements and tool settings; `uv.lock`
   records the exact resolved dependency graph; `.venv` is the generated local
   installation of those dependencies.
10. It prevents CI from silently resolving or writing a different lockfile and
    exposes mismatch between project declarations and the committed lock.
11. Its string length is three. `min_length` does not assign semantic meaning
    to whitespace, so the custom validator must inspect `value.strip()`.
12. FastAPI returns 422, and the route does not run because validation fails at
    the request boundary.
13. `pytest.mark.parametrize` creates one test case for `""` and another for
    `"   "`.
14. No. It exercises HTTP routing, middleware, request validation, route logic,
    the service call, response validation, and serialization in-process.
15. It proved the test could detect the missing observable behavior before the
    implementation existed.
16. Parse the value with `UUID(...)`, assert its expected UUID version, and send
    two requests to assert different values. Propagation behavior could also be
    tested if the design later accepts incoming IDs.

## C. Docker, Compose, and CI

17. An image is an immutable packaged filesystem and configuration template; a
    container is a running or stopped instance created from an image.
18. Docker can reuse the dependency-install layer when source changes but
    dependency declarations do not, making rebuilds faster.
19. Running as an unprivileged user reduces the impact of a compromised process
    and follows least privilege.
20. No. `EXPOSE` documents metadata. `docker run --publish` or Compose `ports`
    creates the host mapping.
21. `.dockerignore` controls the build context sent to Docker; `.gitignore`
    controls untracked files Git normally reports and adds. A file may need to
    be excluded by both systems for different reasons.
22. Lima manages the Linux VM; Colima configures the VM and container runtime;
    Docker Engine builds and runs containers inside Linux; Docker CLI sends
    commands to the engine; Compose applies a declarative multi-service runtime
    configuration.
23. Compose mounts `/tmp` as a writable in-memory `tmpfs`, while the rest of the
    container filesystem remains read-only.
24. On a temporary GitHub-hosted Ubuntu runner, not on the developer's Mac.
25. Passing tests does not prove that the production Dockerfile, build context,
    production-only dependency set, imports, user permissions, or image base
    can build successfully.

## D. Git and operations

26. The working tree contains current files; the staging area contains the
    proposed next snapshot; the local repository stores commits; the remote
    repository is the separately hosted commit/branch state, such as GitHub.
27. Git found no whitespace errors in the unstaged changes being checked. A
    silent command is successful when its exit status is zero.
28. Push the local commit to the tracked remote branch with `git push`.
29. Git preserves history and distributes it to collaborators, while Docker may
    copy build-context contents into layers. Removing a secret from the latest
    file does not reliably remove it from either history.
30. It correlates events but does not prove identity or authorization. Clients
    can observe it, and some designs allow clients to submit one.

## E. Scenarios

31. Inspect pytest's `pythonpath = ["src"]` configuration and how the package is
    installed or exposed in CI. Also inspect the working directory, checkout,
    dependency synchronization, package filenames, and missing `__init__.py`
    files.
32. Add an explicit request timeout, cancellation behavior, a total retry
    budget, and classification of retryable errors. Then use bounded retries
    with exponential backoff and jitter. Blindly retrying a hung call can
    multiply load and cost.
33. Idempotency. An idempotency key and persisted operation result can ensure a
    repeated logical request does not create a second charge or job.
34. Examples include: tests use `src` through pytest configuration while the
    image has a wrong `PYTHONPATH`; a production dependency was incorrectly put
    in the dev group; the non-root user lacks permission; an environment
    variable is missing; the Uvicorn import path or command is wrong; tests did
    not start the actual container process.
35. Schema validation proves structure and types, not truth or usefulness. The
    project needs AI evaluations using representative cases and criteria such
    as correctness, groundedness, relevance, safety, latency, and cost.

## Practical exercise guidance

1. A correct drawing separates server, middleware, routing, validation,
   services, and response serialization.
2. Empty and whitespace-only prompts return 422. A valid four-word prompt
   returns 200 with `word_count: 4` and the exact character count of the input.
3. Your explanation should cover both what each instruction does and why its
   order affects caching, security, or runtime behavior.
4. One possible assertion is:

   ```python
   from uuid import UUID

   request_id = response.headers["x-request-id"]
   assert UUID(request_id).version == 4
   ```

5. Make two requests and assert their `x-request-id` header values differ.
6. A minimal provider-neutral contract accepts a typed request and returns a
   typed result asynchronously. The result might include generated text, model
   identity, token usage, and finish reason. Provider-specific SDK objects and
   exceptions should be translated at the adapter boundary.

## Scoring rubric

- **31-35 correct:** Strong command of the current project; move into design
  tradeoffs and AI-provider integration.
- **25-30 correct:** Good foundation; revisit scenario reasoning and runtime
  boundaries.
- **18-24 correct:** Re-read the architecture, packaging, Docker, and testing
  modules, then retake one section at a time.
- **Below 18:** Work module by module and explain each linked file aloud before
  retrying the quiz.

Do not count a guessed answer as mastered. You should be able to explain why an
alternative is wrong and connect the concept to a specific project file.
