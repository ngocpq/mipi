private void combinator(char combinator) {
        tq.consumeWhitespace();
        String subQuery = consumeSubQuery(); // support multi > childs
        Evaluator e;

        if (evals.size() == 1)
            e = evals.get(0);
        else
            e = new CombiningEvaluator.And(evals);
        evals.clear();
        Evaluator f = parse(subQuery);

        if (combinator == '>')
            evals.add(new CombiningEvaluator.And(f, new StructuralEvaluator.ImmediateParent(e)));
        else if (combinator == ' ')
            evals.add(new CombiningEvaluator.And(f, new StructuralEvaluator.Parent(e)));
        else if (combinator == '+')
            evals.add(new CombiningEvaluator.And(f, new StructuralEvaluator.ImmediatePreviousSibling(e)));
        else if (combinator == '~')
            evals.add(new CombiningEvaluator.And(f, new StructuralEvaluator.PreviousSibling(e)));
        else
            throw new Selector.SelectorParseException("Unknown combinator: " + combinator);
    }