# SQL validator for python (wip)

### Roadmap v1.0
- [ ] It should only work for sql basic syntax (for this version)
- [ ] Parse sql sentence to a tree structure to validate if it's a valid sentence
- [ ] Parse tree structure to sql sentence to validate if syncronization is equivalent 
- [ ] Validate the basic structure for update sentence (in progress)
- [ ] Validate the basic structure for select sentence
- [ ] Validate the basic structure for delete sentence
- [ ] Validate the basic structure for insert sentence
- [ ] Add optional rules:
    - [ ] 1. not allow "delete" without where
    - [ ] 2. not allow "update" without where
    - [ ] 3. not allow "truncate", "drop", "alter", "grant", "create" sentences
    - [ ] 4. Each sentence should end with ";"
    - [ ] 5. not allow repeated reserved keywords
    - [ ] 6. etc...
