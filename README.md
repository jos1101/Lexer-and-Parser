# Lexer-and-Parser

The prograam will return takes a command line .txt file and returns "ACCEPT" or "REJECT" based on the grammar rules below. 

Grammar with left recursion and left factoring issues resolved.

program -> declaration-list
    declaration-list -> declaration declaration-list'
         declaration -> var-declaration
                      | fun-declaration
     var-declaration -> type-specifier ID var-declaration'
      type-specifier -> int
                      | void
                      | float
     fun-declaration -> int ID ( params ) compound-stmt
                      | void ID ( params ) compound-stmt
                      | float ID ( params ) compound-stmt
              params -> param-list
                      | void
          param-list -> param param-list'
               param -> int ID param'
                      | void ID param'
                      | float ID param'
       compound-stmt -> { local-declarations statement-list }
  local-declarations -> local-declarations'
      statement-list -> statement-list'
           statement -> expression-stmt
                      | { local-declarations statement-list }
                      | selection-stmt
                      | iteration-stmt
                      | return-stmt
     expression-stmt -> expression ;
                      | ;
      selection-stmt -> if ( expression ) statement selection-stmt'
      iteration-stmt -> while ( expression ) statement
         return-stmt -> return return-stmt'
          expression -> var = expression
                      | simple-expression
                 var -> ID var'
   simple-expression -> additive-expression simple-expression'
               relop -> <=
                      | <
                      | >
                      | >=
                      | ==
                      | !=
 additive-expression -> term additive-expression'
               addop -> +
                      | -
                term -> factor term'
               mulop -> *
                      | /
              factor -> ( expression )
                      | ID var'
                      | call
                      | NUM
                call -> ID ( args )
                args -> arg-list
                      | ϵ
            arg-list -> ID arg-list'''
                      | ( expression ) term' additive-expression' simple-expression' arg-list'
                      | NUM term' additive-expression' simple-expression' arg-list'
    var-declaration' -> ;
                      | [ NUM ] ;
              param' -> ϵ
                      | [ ]
     selection-stmt' -> ϵ
                      | else statement
        return-stmt' -> ID return-stmt'''
                      | ;
                      | ( expression ) term' additive-expression' simple-expression' ;
                      | NUM term' additive-expression' simple-expression' ;
                var' -> ϵ
                      | [ expression ]
  simple-expression' -> <= additive-expression
                      | < additive-expression
                      | > additive-expression
                      | >= additive-expression
                      | == additive-expression
                      | != additive-expression
                      | ϵ
   declaration-list' -> declaration declaration-list'
                      | ϵ
         param-list' -> , param param-list'
                      | ϵ
 local-declarations' -> var-declaration local-declarations'
                      | ϵ
     statement-list' -> statement statement-list'
                      | ϵ
additive-expression' -> addop term additive-expression'
                      | ϵ
               term' -> mulop factor term'
                      | ϵ
           arg-list' -> , expression arg-list'
                      | ϵ
          arg-list'' -> = expression arg-list'
                      | term' additive-expression' simple-expression' arg-list'
         arg-list''' -> var' arg-list''
                      | ( args ) term' additive-expression' simple-expression' arg-list'
       return-stmt'' -> = expression ;
                      | term' additive-expression' simple-expression' ;
      return-stmt''' -> var' return-stmt''
                      | ( args ) term' additive-expression' simple-expression' ;
