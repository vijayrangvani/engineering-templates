# Practice: write the boilerplate yourself

Same files as the templates, but each one has only the **shape** (comments + `TODO`). You write the code.

## How to drill
1. Pick ONE file per session (start with `fastapi-app/app/config.py`, then `db.py`).
2. Write it from the shape. Docs are fine; the reference template is not (not yet).
3. Check it:
   ```bash
   cd practice/fastapi-app
   pip install -r requirements.txt
   pytest -q            # all 4 tests pass when config, db, models, schemas, crud, router and main are done
   ```
   YAML: `docker compose config` / `kubectl apply --dry-run=client -f deployment.yaml`
4. Only then compare with the reference and note what you missed.
5. Redo the same file a week later from a blank file. When you can do it without looking, move on.

## Reset to blank
```bash
git checkout -- practice/      # throws away your answers, back to the TODO version
```
Tip: practise on a branch (`git switch -c drill-1`) so `main` stays clean.
