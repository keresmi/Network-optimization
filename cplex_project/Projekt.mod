/*********************************************
 * OPL 12.7.1.0 Model
 * Author: Ania
 * Creation Date: 9 gru 2017 at 11:07:41
 *********************************************/
int max_modules = 10;
{string} Nodes = ...;

 tuple Arc {
 	string src;	//wêze³ pocz¹tkowy
 	string dst;	//wêze³ koñcowy 
 	int cap; 	//rozmiar przep³ywnoœci dla jednego modu³u [Gbit/s], wczeœniej oznaczona jako M 
 	int cost; 	// koszt dodania ³¹cza 
 	int base_topo; // 1 jeœli ³¹cze istnieje w pocz¹tkowej topologii 
 }
 
 tuple Demand {
   	string src;	//wêze³ pocz¹tkowy
 	string dst;	//wêze³ koñcowy 
 	int volume; // wartoœæ zapotrzebowania, wczeœniej oznaczona jako h[d]
}
 
 {Arc} Arcs with src in Nodes, dst in Nodes = ...;
 
 {Demand} Demands with src in Nodes, dst in Nodes = ...;
 
 int B = 100000;	//bud¿et
 
 dvar float+ x[Arcs][Demands];	//wielkoœæ przep³ywu realizuj¹cego zapotrzebowanie d 
 dvar float+ y[Arcs];		//przep³ywnoœæ do u¿ycia na ³¹czu e 
 dvar int+ u[Arcs]; 		//liczba ³¹czy do zainstalowania miêdzy dwoma wêz³ami
 
minimize sum(arc in Arcs) arc.cost * u[arc] ;


subject to {

//	budget: sum(e in Arcs) e.cost*u[e] <= B;

	forall(e in Arcs){

	maximum_modules:	u[e] + e.base_topo <= max_modules; //max liczba modu³ów do zamontowania na ³¹czu

	budget:			  	sum(a in Arcs) a.cost*u[a] <= B;

	flows_on_link: 	  	sum(d in Demands) x[e][d] == y[e];

	capacity:		  	y[e] <= e.cap * (u[e] + e.base_topo);
	   
	}

 	forall(d in Demands){
 		forall(v in Nodes){
 			if(d.src == v)
 				sum(e in Arcs : e.src == v) x[e][d] - sum(e in Arcs : e.dst == v) x[e][d] == d.volume;
 			if(d.dst == v)
 				sum(e in Arcs : e.src == v) x[e][d] - sum(e in Arcs : e.dst == v) x[e][d] == -d.volume; 
 			if(d.src != v && d.dst != v)
 				sum(e in Arcs : e.src == v) x[e][d] - sum(e in Arcs : e.dst == v) x[e][d] == 0;  
 		} 	
 	}
}

execute{
	for (var e in Arcs) {
  		write("<"+ e.src +"," + e.dst +"> nb of links:" + u[e] + e.base_topo + " cost:" + u[e]*e.cost + "\n")
  }
}