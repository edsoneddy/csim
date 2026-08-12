# Generated from Java24Parser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .Java24Parser import Java24Parser
else:
    from Java24Parser import Java24Parser

# This class defines a complete generic visitor for a parse tree produced by Java24Parser.

class Java24ParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by Java24Parser#compilationUnit.
    def visitCompilationUnit(self, ctx:Java24Parser.CompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#modularCompulationUnit.
    def visitModularCompulationUnit(self, ctx:Java24Parser.ModularCompulationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#packageDeclaration.
    def visitPackageDeclaration(self, ctx:Java24Parser.PackageDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#importDeclaration.
    def visitImportDeclaration(self, ctx:Java24Parser.ImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:Java24Parser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#modifier.
    def visitModifier(self, ctx:Java24Parser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#classOrInterfaceModifier.
    def visitClassOrInterfaceModifier(self, ctx:Java24Parser.ClassOrInterfaceModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#variableModifier.
    def visitVariableModifier(self, ctx:Java24Parser.VariableModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#classDeclaration.
    def visitClassDeclaration(self, ctx:Java24Parser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeParameters.
    def visitTypeParameters(self, ctx:Java24Parser.TypeParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeParameter.
    def visitTypeParameter(self, ctx:Java24Parser.TypeParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeBound.
    def visitTypeBound(self, ctx:Java24Parser.TypeBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#enumDeclaration.
    def visitEnumDeclaration(self, ctx:Java24Parser.EnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#enumConstants.
    def visitEnumConstants(self, ctx:Java24Parser.EnumConstantsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#enumConstant.
    def visitEnumConstant(self, ctx:Java24Parser.EnumConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#enumBodyDeclarations.
    def visitEnumBodyDeclarations(self, ctx:Java24Parser.EnumBodyDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#interfaceDeclaration.
    def visitInterfaceDeclaration(self, ctx:Java24Parser.InterfaceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#classBody.
    def visitClassBody(self, ctx:Java24Parser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#interfaceBody.
    def visitInterfaceBody(self, ctx:Java24Parser.InterfaceBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#classBodyDeclaration.
    def visitClassBodyDeclaration(self, ctx:Java24Parser.ClassBodyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#memberDeclaration.
    def visitMemberDeclaration(self, ctx:Java24Parser.MemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:Java24Parser.MethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#methodBody.
    def visitMethodBody(self, ctx:Java24Parser.MethodBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeTypeOrVoid.
    def visitTypeTypeOrVoid(self, ctx:Java24Parser.TypeTypeOrVoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#genericMethodDeclaration.
    def visitGenericMethodDeclaration(self, ctx:Java24Parser.GenericMethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#genericConstructorDeclaration.
    def visitGenericConstructorDeclaration(self, ctx:Java24Parser.GenericConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#constructorDeclaration.
    def visitConstructorDeclaration(self, ctx:Java24Parser.ConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#compactConstructorDeclaration.
    def visitCompactConstructorDeclaration(self, ctx:Java24Parser.CompactConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx:Java24Parser.FieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#interfaceBodyDeclaration.
    def visitInterfaceBodyDeclaration(self, ctx:Java24Parser.InterfaceBodyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#interfaceMemberDeclaration.
    def visitInterfaceMemberDeclaration(self, ctx:Java24Parser.InterfaceMemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#constDeclaration.
    def visitConstDeclaration(self, ctx:Java24Parser.ConstDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#constantDeclarator.
    def visitConstantDeclarator(self, ctx:Java24Parser.ConstantDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#interfaceMethodDeclaration.
    def visitInterfaceMethodDeclaration(self, ctx:Java24Parser.InterfaceMethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#interfaceMethodModifier.
    def visitInterfaceMethodModifier(self, ctx:Java24Parser.InterfaceMethodModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#genericInterfaceMethodDeclaration.
    def visitGenericInterfaceMethodDeclaration(self, ctx:Java24Parser.GenericInterfaceMethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#interfaceCommonBodyDeclaration.
    def visitInterfaceCommonBodyDeclaration(self, ctx:Java24Parser.InterfaceCommonBodyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#variableDeclarators.
    def visitVariableDeclarators(self, ctx:Java24Parser.VariableDeclaratorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#variableDeclarator.
    def visitVariableDeclarator(self, ctx:Java24Parser.VariableDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#variableDeclaratorId.
    def visitVariableDeclaratorId(self, ctx:Java24Parser.VariableDeclaratorIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#variableInitializer.
    def visitVariableInitializer(self, ctx:Java24Parser.VariableInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#arrayInitializer.
    def visitArrayInitializer(self, ctx:Java24Parser.ArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#classType.
    def visitClassType(self, ctx:Java24Parser.ClassTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#packageName.
    def visitPackageName(self, ctx:Java24Parser.PackageNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeArgument.
    def visitTypeArgument(self, ctx:Java24Parser.TypeArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#qualifiedNameList.
    def visitQualifiedNameList(self, ctx:Java24Parser.QualifiedNameListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#formalParameters.
    def visitFormalParameters(self, ctx:Java24Parser.FormalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#receiverParameter.
    def visitReceiverParameter(self, ctx:Java24Parser.ReceiverParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#formalParameterList.
    def visitFormalParameterList(self, ctx:Java24Parser.FormalParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#formalParameter.
    def visitFormalParameter(self, ctx:Java24Parser.FormalParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#lambdaLVTIList.
    def visitLambdaLVTIList(self, ctx:Java24Parser.LambdaLVTIListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#lambdaLVTIParameter.
    def visitLambdaLVTIParameter(self, ctx:Java24Parser.LambdaLVTIParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#qualifiedName.
    def visitQualifiedName(self, ctx:Java24Parser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#literal.
    def visitLiteral(self, ctx:Java24Parser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#integerLiteral.
    def visitIntegerLiteral(self, ctx:Java24Parser.IntegerLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#floatLiteral.
    def visitFloatLiteral(self, ctx:Java24Parser.FloatLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#altAnnotationQualifiedName.
    def visitAltAnnotationQualifiedName(self, ctx:Java24Parser.AltAnnotationQualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotation.
    def visitAnnotation(self, ctx:Java24Parser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationFieldValues.
    def visitAnnotationFieldValues(self, ctx:Java24Parser.AnnotationFieldValuesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationFieldValue.
    def visitAnnotationFieldValue(self, ctx:Java24Parser.AnnotationFieldValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationValue.
    def visitAnnotationValue(self, ctx:Java24Parser.AnnotationValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#elementValue.
    def visitElementValue(self, ctx:Java24Parser.ElementValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#elementValueArrayInitializer.
    def visitElementValueArrayInitializer(self, ctx:Java24Parser.ElementValueArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationTypeDeclaration.
    def visitAnnotationTypeDeclaration(self, ctx:Java24Parser.AnnotationTypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationTypeBody.
    def visitAnnotationTypeBody(self, ctx:Java24Parser.AnnotationTypeBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationTypeElementDeclaration.
    def visitAnnotationTypeElementDeclaration(self, ctx:Java24Parser.AnnotationTypeElementDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationTypeElementRest.
    def visitAnnotationTypeElementRest(self, ctx:Java24Parser.AnnotationTypeElementRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationMethodOrConstantRest.
    def visitAnnotationMethodOrConstantRest(self, ctx:Java24Parser.AnnotationMethodOrConstantRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationMethodRest.
    def visitAnnotationMethodRest(self, ctx:Java24Parser.AnnotationMethodRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#annotationConstantRest.
    def visitAnnotationConstantRest(self, ctx:Java24Parser.AnnotationConstantRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#defaultValue.
    def visitDefaultValue(self, ctx:Java24Parser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#moduleDeclaration.
    def visitModuleDeclaration(self, ctx:Java24Parser.ModuleDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#moduleDirective.
    def visitModuleDirective(self, ctx:Java24Parser.ModuleDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#requiresModifier.
    def visitRequiresModifier(self, ctx:Java24Parser.RequiresModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#recordDeclaration.
    def visitRecordDeclaration(self, ctx:Java24Parser.RecordDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#recordHeader.
    def visitRecordHeader(self, ctx:Java24Parser.RecordHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#recordComponentList.
    def visitRecordComponentList(self, ctx:Java24Parser.RecordComponentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#recordComponent.
    def visitRecordComponent(self, ctx:Java24Parser.RecordComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#recordBody.
    def visitRecordBody(self, ctx:Java24Parser.RecordBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#block.
    def visitBlock(self, ctx:Java24Parser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#blockStatement.
    def visitBlockStatement(self, ctx:Java24Parser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#localVariableDeclaration.
    def visitLocalVariableDeclaration(self, ctx:Java24Parser.LocalVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#identifier.
    def visitIdentifier(self, ctx:Java24Parser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeIdentifier.
    def visitTypeIdentifier(self, ctx:Java24Parser.TypeIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#localTypeDeclaration.
    def visitLocalTypeDeclaration(self, ctx:Java24Parser.LocalTypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#statement.
    def visitStatement(self, ctx:Java24Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#catchClause.
    def visitCatchClause(self, ctx:Java24Parser.CatchClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#catchType.
    def visitCatchType(self, ctx:Java24Parser.CatchTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#finallyBlock.
    def visitFinallyBlock(self, ctx:Java24Parser.FinallyBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#resourceSpecification.
    def visitResourceSpecification(self, ctx:Java24Parser.ResourceSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#resources.
    def visitResources(self, ctx:Java24Parser.ResourcesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#resource.
    def visitResource(self, ctx:Java24Parser.ResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#switchBlockStatementGroup.
    def visitSwitchBlockStatementGroup(self, ctx:Java24Parser.SwitchBlockStatementGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#switchLabel.
    def visitSwitchLabel(self, ctx:Java24Parser.SwitchLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#forControl.
    def visitForControl(self, ctx:Java24Parser.ForControlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#forInit.
    def visitForInit(self, ctx:Java24Parser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#enhancedForControl.
    def visitEnhancedForControl(self, ctx:Java24Parser.EnhancedForControlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#expressionList.
    def visitExpressionList(self, ctx:Java24Parser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#methodCall.
    def visitMethodCall(self, ctx:Java24Parser.MethodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#TernaryExpression.
    def visitTernaryExpression(self, ctx:Java24Parser.TernaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#InstanceOfOperatorExpression.
    def visitInstanceOfOperatorExpression(self, ctx:Java24Parser.InstanceOfOperatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#UnaryOperatorExpression.
    def visitUnaryOperatorExpression(self, ctx:Java24Parser.UnaryOperatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#PrimaryExpression.
    def visitPrimaryExpression(self, ctx:Java24Parser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#ObjectCreationExpression.
    def visitObjectCreationExpression(self, ctx:Java24Parser.ObjectCreationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#ExpressionLambda.
    def visitExpressionLambda(self, ctx:Java24Parser.ExpressionLambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#PostIncrementDecrementOperatorExpression.
    def visitPostIncrementDecrementOperatorExpression(self, ctx:Java24Parser.PostIncrementDecrementOperatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#MemberReferenceExpression.
    def visitMemberReferenceExpression(self, ctx:Java24Parser.MemberReferenceExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#ExpressionSwitch.
    def visitExpressionSwitch(self, ctx:Java24Parser.ExpressionSwitchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#BinaryOperatorExpression.
    def visitBinaryOperatorExpression(self, ctx:Java24Parser.BinaryOperatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#MethodCallExpression.
    def visitMethodCallExpression(self, ctx:Java24Parser.MethodCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#MethodReferenceExpression.
    def visitMethodReferenceExpression(self, ctx:Java24Parser.MethodReferenceExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#SquareBracketExpression.
    def visitSquareBracketExpression(self, ctx:Java24Parser.SquareBracketExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#CastExpression.
    def visitCastExpression(self, ctx:Java24Parser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#pattern.
    def visitPattern(self, ctx:Java24Parser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#componentPatternList.
    def visitComponentPatternList(self, ctx:Java24Parser.ComponentPatternListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#componentPattern.
    def visitComponentPattern(self, ctx:Java24Parser.ComponentPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#lambdaExpression.
    def visitLambdaExpression(self, ctx:Java24Parser.LambdaExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#lambdaParameters.
    def visitLambdaParameters(self, ctx:Java24Parser.LambdaParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#lambdaBody.
    def visitLambdaBody(self, ctx:Java24Parser.LambdaBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#primary.
    def visitPrimary(self, ctx:Java24Parser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#switchExpression.
    def visitSwitchExpression(self, ctx:Java24Parser.SwitchExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#switchLabeledRule.
    def visitSwitchLabeledRule(self, ctx:Java24Parser.SwitchLabeledRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#guard.
    def visitGuard(self, ctx:Java24Parser.GuardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#casePattern.
    def visitCasePattern(self, ctx:Java24Parser.CasePatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#switchRuleOutcome.
    def visitSwitchRuleOutcome(self, ctx:Java24Parser.SwitchRuleOutcomeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#classOrInterfaceType.
    def visitClassOrInterfaceType(self, ctx:Java24Parser.ClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#creator.
    def visitCreator(self, ctx:Java24Parser.CreatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#createdName.
    def visitCreatedName(self, ctx:Java24Parser.CreatedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#innerCreator.
    def visitInnerCreator(self, ctx:Java24Parser.InnerCreatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#arrayCreatorRest.
    def visitArrayCreatorRest(self, ctx:Java24Parser.ArrayCreatorRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#classCreatorRest.
    def visitClassCreatorRest(self, ctx:Java24Parser.ClassCreatorRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#explicitGenericInvocation.
    def visitExplicitGenericInvocation(self, ctx:Java24Parser.ExplicitGenericInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeArgumentsOrDiamond.
    def visitTypeArgumentsOrDiamond(self, ctx:Java24Parser.TypeArgumentsOrDiamondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#nonWildcardTypeArgumentsOrDiamond.
    def visitNonWildcardTypeArgumentsOrDiamond(self, ctx:Java24Parser.NonWildcardTypeArgumentsOrDiamondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#nonWildcardTypeArguments.
    def visitNonWildcardTypeArguments(self, ctx:Java24Parser.NonWildcardTypeArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeList.
    def visitTypeList(self, ctx:Java24Parser.TypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeType.
    def visitTypeType(self, ctx:Java24Parser.TypeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#primitiveType.
    def visitPrimitiveType(self, ctx:Java24Parser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#typeArguments.
    def visitTypeArguments(self, ctx:Java24Parser.TypeArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#superSuffix.
    def visitSuperSuffix(self, ctx:Java24Parser.SuperSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#explicitGenericInvocationSuffix.
    def visitExplicitGenericInvocationSuffix(self, ctx:Java24Parser.ExplicitGenericInvocationSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Java24Parser#arguments.
    def visitArguments(self, ctx:Java24Parser.ArgumentsContext):
        return self.visitChildren(ctx)



del Java24Parser