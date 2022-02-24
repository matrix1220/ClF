#include <string>
#include <iostream>
#include <variant>
#include <vector>

namespace FAL {

	// std::string implode(char separator, ) {
	// }
	class Statement
	{
	public:
		virtual std::string getCode() = 0;
		
	};
	class StatementSet
	{
	public:
		std::vector<Statement> contents;
	};

	class Literal // I
	{
	public:
		int content;
		Literal(int content): content(content) {}
		std::string toString() {return content;}
	};
	class Register // R
	{
	public:
		std::string content;
		Register(int content): content(std::string("mem") + content) {}
		Register(std::string content): content(content) {}
		std::string toString() {return content;}
	};
	enum class Wire // W
	{
		red,
		green
	};
	class Label: public Statement // L
	{
	public:
		std::string name;
		Label(std::string name): name(name) {}
		std::string toString() {return std::string("mem") + content;}
	};
	using I = Literal;
	using R = Register;
	using W = Wire;
	using L = Label;

	template <class... Ts>
	class Content
	{
	public:
		std::variant<Ts...> content;
		template <class T>
		Content(T content): content(content) {}
		std::string toString() {}
		
	};


	class Move: public Statement
	{
	public:
		R source;
		R destination;
		
	};
	class Set: public Statement
	{
	public:
		Content<R,I> source;
		R destination;
		
	};
}
int main() {
	StatementSet temp(
		Move(R::mem1, R::mem2),
		Set(I(1), R:mem11)
		);
}