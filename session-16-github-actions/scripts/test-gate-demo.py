from pathlib import Path
import shutil,subprocess,tempfile,sys
source=Path(__file__).resolve().parent.parent/'session-16-github-actions/10-final-cicd-pipeline'
with tempfile.TemporaryDirectory(prefix='session16-failure-') as temp:
    project=Path(temp)/'calculator'
    shutil.copytree(source,project,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache','build'))
    app=project/'app/calculator.py'; original=app.read_text()
    app.write_text(original.replace('return a + b','return a + b + 1'))
    print('Temporary copy: introduce add() defect; source checkout remains intact.',flush=True)
    failed=subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=project)
    assert failed.returncode==1
    print('Test gate rejected the defective build. Restore add().',flush=True)
    app.write_text(original)
    # Clear cached bytecode to exercise the restored source immediately.
    shutil.rmtree(project/'app/__pycache__',ignore_errors=True)
    subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=project,check=True)
