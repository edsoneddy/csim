# Generated from CParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete generic visitor for a parse tree produced by CParser.

class CParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CParser#compilationUnit.
    def visitCompilationUnit(self, ctx:CParser.CompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#constant.
    def visitConstant(self, ctx:CParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumerationConstant.
    def visitEnumerationConstant(self, ctx:CParser.EnumerationConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#predefinedConstant.
    def visitPredefinedConstant(self, ctx:CParser.PredefinedConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#exprList.
    def visitExprList(self, ctx:CParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#genericSelection.
    def visitGenericSelection(self, ctx:CParser.GenericSelectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#genericAssocList.
    def visitGenericAssocList(self, ctx:CParser.GenericAssocListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#genericAssociation.
    def visitGenericAssociation(self, ctx:CParser.GenericAssociationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#postfixExpression.
    def visitPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#argumentExpressionList.
    def visitArgumentExpressionList(self, ctx:CParser.ArgumentExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryExpression.
    def visitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#castExpression.
    def visitCastExpression(self, ctx:CParser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#shiftExpression.
    def visitShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#relationalExpression.
    def visitRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#equalityExpression.
    def visitEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#andExpression.
    def visitAndExpression(self, ctx:CParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#exclusiveOrExpression.
    def visitExclusiveOrExpression(self, ctx:CParser.ExclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#inclusiveOrExpression.
    def visitInclusiveOrExpression(self, ctx:CParser.InclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx:CParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#constantExpression.
    def visitConstantExpression(self, ctx:CParser.ConstantExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declaration.
    def visitDeclaration(self, ctx:CParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarationSpecifiers.
    def visitDeclarationSpecifiers(self, ctx:CParser.DeclarationSpecifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarationSpecifier.
    def visitDeclarationSpecifier(self, ctx:CParser.DeclarationSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initDeclaratorList.
    def visitInitDeclaratorList(self, ctx:CParser.InitDeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initDeclarator.
    def visitInitDeclarator(self, ctx:CParser.InitDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#attributeDeclaration.
    def visitAttributeDeclaration(self, ctx:CParser.AttributeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#storageClassSpecifier.
    def visitStorageClassSpecifier(self, ctx:CParser.StorageClassSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structOrUnionSpecifier.
    def visitStructOrUnionSpecifier(self, ctx:CParser.StructOrUnionSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structOrUnion.
    def visitStructOrUnion(self, ctx:CParser.StructOrUnionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#memberDeclarationList.
    def visitMemberDeclarationList(self, ctx:CParser.MemberDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#memberDeclaration.
    def visitMemberDeclaration(self, ctx:CParser.MemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#specifierQualifierList.
    def visitSpecifierQualifierList(self, ctx:CParser.SpecifierQualifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeSpecifierQualifier.
    def visitTypeSpecifierQualifier(self, ctx:CParser.TypeSpecifierQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#memberDeclaratorList.
    def visitMemberDeclaratorList(self, ctx:CParser.MemberDeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#memberDeclarator.
    def visitMemberDeclarator(self, ctx:CParser.MemberDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumSpecifier.
    def visitEnumSpecifier(self, ctx:CParser.EnumSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumeratorList.
    def visitEnumeratorList(self, ctx:CParser.EnumeratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumerator.
    def visitEnumerator(self, ctx:CParser.EnumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumTypeSpecifier.
    def visitEnumTypeSpecifier(self, ctx:CParser.EnumTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#atomicTypeSpecifier.
    def visitAtomicTypeSpecifier(self, ctx:CParser.AtomicTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeofSpecifier.
    def visitTypeofSpecifier(self, ctx:CParser.TypeofSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeofSpecifierArgument.
    def visitTypeofSpecifierArgument(self, ctx:CParser.TypeofSpecifierArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeQualifier.
    def visitTypeQualifier(self, ctx:CParser.TypeQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionSpecifier.
    def visitFunctionSpecifier(self, ctx:CParser.FunctionSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#alignmentSpecifier.
    def visitAlignmentSpecifier(self, ctx:CParser.AlignmentSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarator.
    def visitDeclarator(self, ctx:CParser.DeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#directDeclarator.
    def visitDirectDeclarator(self, ctx:CParser.DirectDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#pointer.
    def visitPointer(self, ctx:CParser.PointerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeQualifierList.
    def visitTypeQualifierList(self, ctx:CParser.TypeQualifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameterTypeList.
    def visitParameterTypeList(self, ctx:CParser.ParameterTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameterList.
    def visitParameterList(self, ctx:CParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:CParser.ParameterDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeName.
    def visitTypeName(self, ctx:CParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#abstractDeclarator.
    def visitAbstractDeclarator(self, ctx:CParser.AbstractDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#directAbstractDeclarator.
    def visitDirectAbstractDeclarator(self, ctx:CParser.DirectAbstractDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typedefName.
    def visitTypedefName(self, ctx:CParser.TypedefNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initializer.
    def visitInitializer(self, ctx:CParser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initializerList.
    def visitInitializerList(self, ctx:CParser.InitializerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#designation.
    def visitDesignation(self, ctx:CParser.DesignationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#designatorList.
    def visitDesignatorList(self, ctx:CParser.DesignatorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#designator.
    def visitDesignator(self, ctx:CParser.DesignatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#staticAssertDeclaration.
    def visitStaticAssertDeclaration(self, ctx:CParser.StaticAssertDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#attributeSpecifierSequence.
    def visitAttributeSpecifierSequence(self, ctx:CParser.AttributeSpecifierSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#attributeSpecifier.
    def visitAttributeSpecifier(self, ctx:CParser.AttributeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#attributeList.
    def visitAttributeList(self, ctx:CParser.AttributeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#attribute.
    def visitAttribute(self, ctx:CParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#attributeToken.
    def visitAttributeToken(self, ctx:CParser.AttributeTokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#attributeArgumentClause.
    def visitAttributeArgumentClause(self, ctx:CParser.AttributeArgumentClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#balancedTokenSequence.
    def visitBalancedTokenSequence(self, ctx:CParser.BalancedTokenSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#balancedToken.
    def visitBalancedToken(self, ctx:CParser.BalancedTokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#labeledStatement.
    def visitLabeledStatement(self, ctx:CParser.LabeledStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compoundStatement.
    def visitCompoundStatement(self, ctx:CParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#blockItemList.
    def visitBlockItemList(self, ctx:CParser.BlockItemListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#blockItem.
    def visitBlockItem(self, ctx:CParser.BlockItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expressionStatement.
    def visitExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#selectionStatement.
    def visitSelectionStatement(self, ctx:CParser.SelectionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#iterationStatement.
    def visitIterationStatement(self, ctx:CParser.IterationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forCondition.
    def visitForCondition(self, ctx:CParser.ForConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forDeclaration.
    def visitForDeclaration(self, ctx:CParser.ForDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forExpression.
    def visitForExpression(self, ctx:CParser.ForExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#jumpStatement.
    def visitJumpStatement(self, ctx:CParser.JumpStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#translationUnit.
    def visitTranslationUnit(self, ctx:CParser.TranslationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#externalDeclaration.
    def visitExternalDeclaration(self, ctx:CParser.ExternalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:CParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarationList.
    def visitDeclarationList(self, ctx:CParser.DeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionBody.
    def visitFunctionBody(self, ctx:CParser.FunctionBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#identifierList.
    def visitIdentifierList(self, ctx:CParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gnuArrayDesignator.
    def visitGnuArrayDesignator(self, ctx:CParser.GnuArrayDesignatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gnuIdentifier.
    def visitGnuIdentifier(self, ctx:CParser.GnuIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asmArgument.
    def visitAsmArgument(self, ctx:CParser.AsmArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asmClobbers.
    def visitAsmClobbers(self, ctx:CParser.AsmClobbersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asmDefinition.
    def visitAsmDefinition(self, ctx:CParser.AsmDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asm_.
    def visitAsm_(self, ctx:CParser.Asm_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#toplevelAsmArgument.
    def visitToplevelAsmArgument(self, ctx:CParser.ToplevelAsmArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asmOperand.
    def visitAsmOperand(self, ctx:CParser.AsmOperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asmOperands.
    def visitAsmOperands(self, ctx:CParser.AsmOperandsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asmQualifier.
    def visitAsmQualifier(self, ctx:CParser.AsmQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#volatile_.
    def visitVolatile_(self, ctx:CParser.Volatile_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asmQualifierList.
    def visitAsmQualifierList(self, ctx:CParser.AsmQualifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asmStatement.
    def visitAsmStatement(self, ctx:CParser.AsmStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#asmStringLiteral.
    def visitAsmStringLiteral(self, ctx:CParser.AsmStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gccDeclaratorExtension.
    def visitGccDeclaratorExtension(self, ctx:CParser.GccDeclaratorExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gnuAttribute.
    def visitGnuAttribute(self, ctx:CParser.GnuAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gnuAttributeList.
    def visitGnuAttributeList(self, ctx:CParser.GnuAttributeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gnuAttributes.
    def visitGnuAttributes(self, ctx:CParser.GnuAttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gnuSingleAttribute.
    def visitGnuSingleAttribute(self, ctx:CParser.GnuSingleAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#simpleAsmExpr.
    def visitSimpleAsmExpr(self, ctx:CParser.SimpleAsmExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#vcSpecificModifer.
    def visitVcSpecificModifer(self, ctx:CParser.VcSpecificModiferContext):
        return self.visitChildren(ctx)



del CParser