#include <iostream>
#include <vector>
#include <variant>

using EvaluatingResult = std::variant<int, >;
class Expression
{
public:
	Expression(){}
	virtual Pointer evaluate() = 0;
	
};
class Integer
{
public:
	int content;
	Integer(int content): content(content) {}
	int evaluate() {}
	
};

class Pointer
{
public:
	unsigned short int cell;
	Pointer(int cell) { this->cell = cell; }
	
};

class IntegerOperation: public Expression
{
public:
	Integer* left;
	Integer* right;
	IntegerOperation(Integer* left, Integer* right): left(left), right(right) {}
};

class Adddition: public IntegerOperation
{
public:
	using IntegerOperation::IntegerOperation;
	
	
};

class Boolean
{
public:
	virtual EvaluatingResult evaluate() = 0;
};

class BooleanOperation: public Boolean
{
	Boolean* left;
	Boolean* right;
public:

	
};

class LogicAnd: public BooleanOperation
{
public:
	
};

class Condition: public Boolean
{
public:
	Condition(){}
	
};

class Statement
{
public:
	Statement* parent = nullptr;
	Statement() {}
	//virtual getFAL();
	//std::map<std::string, Variable> variables;
	
};

class Block: public Statement
{
public:
	std::vector<Statement*> contents;
};

class ifStatement: Statement
{
public:
	Boolean* condition;
	Statement* positive;
	Statement* negative;
	ifStatement(Boolean* condition, Statement* positive, Statement* negative):
	condition(condition), positive(positive), negative(negative) {}
	
};

class Assignment: Statement
{
public:
	std::variant<Integer, Pointer> source;
	Pointer destination;
	
};

int main() {
	Block main;
	Pointer status(11);

	ifStatement ifstatement(main, LessThan(1,Pointer(11)));
	return 0;
}