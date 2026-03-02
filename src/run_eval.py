import argparse
from evaluator import run_evaluation

def main():
    parser = argparse.ArgumentParser(description='Run AI evaluation harness')
    parser.add_argument('--test-cases', required=True)
    parser.add_argument('--gold', required=True)
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    metrics = run_evaluation(args.test_cases, args.gold, args.out_dir)
    print('Evaluation complete. Metrics saved to', args.out_dir)
    print(metrics['summary'])

if __name__ == '__main__':
    main()
# BEFORE
from evaluator import run_evaluation

# AFTER
from src.evaluator import run_evaluation
