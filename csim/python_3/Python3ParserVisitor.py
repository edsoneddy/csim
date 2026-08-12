# Generated from Python3Parser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .Python3Parser import Python3Parser
else:
    from Python3Parser import Python3Parser

# This class defines a complete generic visitor for a parse tree produced by Python3Parser.

class Python3ParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by Python3Parser#root.
    def visitRoot(self, ctx:Python3Parser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#single_input.
    def visitSingle_input(self, ctx:Python3Parser.Single_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#file_input.
    def visitFile_input(self, ctx:Python3Parser.File_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#eval_input.
    def visitEval_input(self, ctx:Python3Parser.Eval_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#stmt.
    def visitStmt(self, ctx:Python3Parser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#if_stmt.
    def visitIf_stmt(self, ctx:Python3Parser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#while_stmt.
    def visitWhile_stmt(self, ctx:Python3Parser.While_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#for_stmt.
    def visitFor_stmt(self, ctx:Python3Parser.For_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#try_stmt.
    def visitTry_stmt(self, ctx:Python3Parser.Try_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#with_stmt.
    def visitWith_stmt(self, ctx:Python3Parser.With_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#class_or_func_def_stmt.
    def visitClass_or_func_def_stmt(self, ctx:Python3Parser.Class_or_func_def_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#suite.
    def visitSuite(self, ctx:Python3Parser.SuiteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorator.
    def visitDecorator(self, ctx:Python3Parser.DecoratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#elif_clause.
    def visitElif_clause(self, ctx:Python3Parser.Elif_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#else_clause.
    def visitElse_clause(self, ctx:Python3Parser.Else_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#finally_clause.
    def visitFinally_clause(self, ctx:Python3Parser.Finally_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#with_item.
    def visitWith_item(self, ctx:Python3Parser.With_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#except_clause.
    def visitExcept_clause(self, ctx:Python3Parser.Except_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#classdef.
    def visitClassdef(self, ctx:Python3Parser.ClassdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#funcdef.
    def visitFuncdef(self, ctx:Python3Parser.FuncdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#typedargslist.
    def visitTypedargslist(self, ctx:Python3Parser.TypedargslistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#args.
    def visitArgs(self, ctx:Python3Parser.ArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#kwargs.
    def visitKwargs(self, ctx:Python3Parser.KwargsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#def_parameters.
    def visitDef_parameters(self, ctx:Python3Parser.Def_parametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#def_parameter.
    def visitDef_parameter(self, ctx:Python3Parser.Def_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#named_parameter.
    def visitNamed_parameter(self, ctx:Python3Parser.Named_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#simple_stmt.
    def visitSimple_stmt(self, ctx:Python3Parser.Simple_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#expr_stmt.
    def visitExpr_stmt(self, ctx:Python3Parser.Expr_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#print_stmt.
    def visitPrint_stmt(self, ctx:Python3Parser.Print_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#del_stmt.
    def visitDel_stmt(self, ctx:Python3Parser.Del_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#pass_stmt.
    def visitPass_stmt(self, ctx:Python3Parser.Pass_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#break_stmt.
    def visitBreak_stmt(self, ctx:Python3Parser.Break_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#continue_stmt.
    def visitContinue_stmt(self, ctx:Python3Parser.Continue_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#return_stmt.
    def visitReturn_stmt(self, ctx:Python3Parser.Return_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#raise_stmt.
    def visitRaise_stmt(self, ctx:Python3Parser.Raise_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yield_stmt.
    def visitYield_stmt(self, ctx:Python3Parser.Yield_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_stmt.
    def visitImport_stmt(self, ctx:Python3Parser.Import_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#from_stmt.
    def visitFrom_stmt(self, ctx:Python3Parser.From_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#global_stmt.
    def visitGlobal_stmt(self, ctx:Python3Parser.Global_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#exec_stmt.
    def visitExec_stmt(self, ctx:Python3Parser.Exec_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#assert_stmt.
    def visitAssert_stmt(self, ctx:Python3Parser.Assert_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#nonlocal_stmt.
    def visitNonlocal_stmt(self, ctx:Python3Parser.Nonlocal_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist_star_expr.
    def visitTestlist_star_expr(self, ctx:Python3Parser.Testlist_star_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#star_expr.
    def visitStar_expr(self, ctx:Python3Parser.Star_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#assign_part.
    def visitAssign_part(self, ctx:Python3Parser.Assign_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#exprlist.
    def visitExprlist(self, ctx:Python3Parser.ExprlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_as_names.
    def visitImport_as_names(self, ctx:Python3Parser.Import_as_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_as_name.
    def visitImport_as_name(self, ctx:Python3Parser.Import_as_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dotted_as_names.
    def visitDotted_as_names(self, ctx:Python3Parser.Dotted_as_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dotted_as_name.
    def visitDotted_as_name(self, ctx:Python3Parser.Dotted_as_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#test.
    def visitTest(self, ctx:Python3Parser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#varargslist.
    def visitVarargslist(self, ctx:Python3Parser.VarargslistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#vardef_parameters.
    def visitVardef_parameters(self, ctx:Python3Parser.Vardef_parametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#vardef_parameter.
    def visitVardef_parameter(self, ctx:Python3Parser.Vardef_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#varargs.
    def visitVarargs(self, ctx:Python3Parser.VarargsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#varkwargs.
    def visitVarkwargs(self, ctx:Python3Parser.VarkwargsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#logical_test.
    def visitLogical_test(self, ctx:Python3Parser.Logical_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comparison.
    def visitComparison(self, ctx:Python3Parser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#expr.
    def visitExpr(self, ctx:Python3Parser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom.
    def visitAtom(self, ctx:Python3Parser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dictorsetmaker.
    def visitDictorsetmaker(self, ctx:Python3Parser.DictorsetmakerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist_comp.
    def visitTestlist_comp(self, ctx:Python3Parser.Testlist_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist.
    def visitTestlist(self, ctx:Python3Parser.TestlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dotted_name.
    def visitDotted_name(self, ctx:Python3Parser.Dotted_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#name.
    def visitName(self, ctx:Python3Parser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#number.
    def visitNumber(self, ctx:Python3Parser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#integer.
    def visitInteger(self, ctx:Python3Parser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yield_expr.
    def visitYield_expr(self, ctx:Python3Parser.Yield_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yield_arg.
    def visitYield_arg(self, ctx:Python3Parser.Yield_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#trailer.
    def visitTrailer(self, ctx:Python3Parser.TrailerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arguments.
    def visitArguments(self, ctx:Python3Parser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arglist.
    def visitArglist(self, ctx:Python3Parser.ArglistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#argument.
    def visitArgument(self, ctx:Python3Parser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscriptlist.
    def visitSubscriptlist(self, ctx:Python3Parser.SubscriptlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscript.
    def visitSubscript(self, ctx:Python3Parser.SubscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#sliceop.
    def visitSliceop(self, ctx:Python3Parser.SliceopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comp_for.
    def visitComp_for(self, ctx:Python3Parser.Comp_forContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comp_iter.
    def visitComp_iter(self, ctx:Python3Parser.Comp_iterContext):
        return self.visitChildren(ctx)



del Python3Parser