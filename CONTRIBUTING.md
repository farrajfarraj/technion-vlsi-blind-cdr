# Working together

Each student signs in to GitHub with their own account. The repository owner can invite the partner through **Settings → Collaborators → Add people**. Select the partner's confirmed username. After accepting the invitation, the partner can clone the private repository and push a feature branch. [GitHub collaborator instructions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository)

## First checkout

Copy the repository's HTTPS clone URL from **Code**. In PowerShell, replace the placeholder in the first line with that URL.

```powershell
git clone <repository-HTTPS-URL>
cd technion-vlsi-blind-cdr
git config --get user.name
git config --get user.email
```

If needed, set the Git author name and a verified GitHub email or GitHub-provided noreply address for this checkout. Each student's commits should carry their own identity. Obtain the model, open the inverter, and check it before running the flip-flop. [LTspice setup](docs/setup-instructions.md)

## One experiment per pull request

1. Pick or open an issue with a measurement question and acceptance criteria. A good first contribution is independent reproduction of the six-edge flip-flop test.
2. Start from the reviewed main branch.

   ```powershell
   git switch main
   git pull --ff-only
   git switch -c experiment/reproduce-flipflop
   ```

3. Record the source revision, simulator version, model fingerprint, operating conditions, sweep parameters, and observed result in the progress log. For a mismatch, record the first differing edge or measurement. Keep raw waveforms locally. Include a portable figure, CSV or small log excerpt sufficient for review.
4. Stage only the relevant paths and inspect the staged diff. For a progress-log update:

   ```powershell
   git add docs/progress-log.md
   git diff --cached
   git commit -m "Record independent flip-flop capture check"
   git push -u origin experiment/reproduce-flipflop
   ```

5. Open a pull request against `main`, link the issue, identify what was rerun, and request the other student's review. Merge after the reviewer checks the evidence. The owner can enable required reviews in repository rules when the account plan and team workflow support them.

Use a new directory under `simulations/` for later milestones. Preserve the reference model hash and conditions for comparisons. Keep third-party models, logs with absolute paths, private discussions, credentials and course materials out of commits. The project begins on private GitHub hosting once provisioned. Changing visibility requires explicit owner approval and a rights review.
