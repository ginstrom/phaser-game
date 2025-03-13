# Backend Test Debugging

- Always run tests in docker-compose
- Prefer using `test.sh backend` as test runner
- If you are asked to test a single test file, use `docker-compose -f docker-compose.test.yml <pytest command>`
- the docker-compose config is in docker-compose.test.yml
- use sqlite in-memory db for unit testing
- If paths are incorrect, fix docker first, test files next. 
- Do not change code structure to fix test errors.