
var alphabet = "abcdefghijklmnopqrstuvwxyz".split("");
var b = 0,
	i = 0;
var bases = ["Warszawa to największe", "Te zabawki należą do", "Policjant przygląda się", 
			 "Na środku skrzyżowania widać", "Właściciel samochodu widział złodzieja z",
			 "Prezydent z premierem rozmawiali wczoraj o", "Gdybym wiedział wtedy dokładnie to, co wiem teraz, to bym się nie",
			 "Gdybym wiedziała wtedy dokładnie to, co wiem teraz, to bym się nie",
			 "Polscy naukowcy odkryli w Tatrach nowy gatunek istoty żywej. Zwięrzę to przypomina małpę, lecz porusza się na dwóch"
			 + "nogach i potrafi posługiwać się narzędziami. Przy dłuższej obserwacji okazało się, że potrafi również posługiwać się"
			 + "językiem polskim, a konkretnie gwarą podhalańską. Zwierzę to zostało nazwane"]
var endings = {
	0: ["miasto", "zabytkowe", "miasto na Górnym Śląsku", "centrum handlowe terenu Legionów i osiem biegunowego",
		"miasto na południu kraju, zamieszkane przez 21 385 osób.. w 1785 r. pojawili się zwyżkami Beast na UK zbrojne członków jednej firmy.."],
	1: ["Dźstoni.", "pierwszorzędnych podświadomych..", "najcenniejszych i dlatego postanowiłam spróbować spodoba Wam się to medium ..",
		"doustnych sklepików sałatkowych.. ażeby zachować ochronność, ponieważ chroni on przed Karmel Acter Y64 czy Hajding God wylewa jabłko z puszek ubiegłorocznym"],
	2: ["220 obywatelom i wykonuje", "Baronowi i ratuje drogę Pedersenowi, rozwiązuje wątpliwości"],
	3: ["ślad", "następne pojawiające się figury na", "głównie fragment półkolisty z laminowanej okienni,", 
		"genetyczne ząbki siewny pękające chwasty jadalne opóźniane zimą odchodzijący przytlenku sodu, którym glukoza uzupełnia błękit w grzebieniu na ten Zawodowiak.."],
	4: ["drabin", "bojarami w sprowadzającym", "wykorzystaniem modulacji Bąkówki, Ciążawojennego popiwk", 
		"krążeniem, wychowawczynią babci, wspomagała mamę, wirusem zakaźnym oraz nowotworami płuc komar",
		"Warszawy i przeżył wypadek .. to już stanowił pasztet dla userów biorarek.. jestex1000l. a my chcemy"],
	5: ["tym", "akcji", "projekcie telewizyjnym, który robiony był tak wątpliwy do tej pory ..", "rozmaitej osji zbrodni indyjskich, karai", 
		"zamknięciu odpowiedzą na zaskoczenie miłośników Terror Lago Holocaust.. z twej trybuny rotacyjnej przeszkadzają sytuacja żołnierzom sprawiającym fali aprecjacji broni wiązkowej"],
	6: ["spodziewał", "ubezpieczał, pewnie wiesz", "odganiał ..", 
		"odwołał.. i wiem, ze wysadzam się w arteri zupełnykulturowość.. o .. lodu update starych mezarsrox pojedzie na Marszałkowska zakłócenia"],
	7: ["spodziewała że to będzie jakiś problem ..", "dowiedziała", "odwoływał bo faktycznie szparagi są wytrawne, przecież", 
		"orucznikiła Atlasowe spódniczki sim Busa Quartera w dobrej cenie, czy nie powinno być maleńki"],
	8: ["Mount", "na cześć", "językami ryżu lokalnego..", "trawą, na", 
		"Oberrum Mondectoris krz Pereus na cześć wybitnego krewnegoBenzobrocusa Be",
		"Rudnicki babcia zapomnij o klechy mojego pasierbiaka dziewczynęstrzału Kołeczek piszesz o wyśmienitym wyglądziebaru infekcje .. ZdobywczyniaWIĄZCZNE"]

}

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var base = svg.append("g")
		.attr("transform", "translate(10," + (height / 2) + ")")
		.attr("y", 40)
		.on("click", function(){
			b++;
			if (b == bases.length) {
				b = 0;
			}
			i = 0;
			update([base, bases[b]]);
			update([g, endings[b][i++]]);
		});

var g = svg.append("g")
		.attr("transform", "translate(10," + (height / 2 + 50) + ")")
		.attr("y", 20)
		.on("click", function(){
			if (i == endings[b].length) {
				i = 0;
			}
			update([g, endings[b][i++]]);
		});

function update([o, data]) {
  var t = d3.transition()
      .duration(750);


  // JOIN new data with old elements.
  var text = o.selectAll("text")
    .data(data, function(d) { return d; });

  // EXIT old elements not present in new data.
  text.exit()
      .attr("class", "exit")
    .transition(t)
      .attr("y", 60)
      .style("fill-opacity", 1e-6)
      .remove();

  // UPDATE old elements present in new data.
  text.attr("class", "update")
      .attr("y", 0)
      .style("fill-opacity", 1)
    .transition(t)
      .attr("x", function(d, i) { return i * 15; });

  // ENTER new elements present in new data.
  text.enter().append("text")
      .attr("class", "enter")
      .attr("dy", ".35em")
      .attr("y", -60)
      .attr("x", function(d, i) { return i * 15; })
      .style("fill-opacity", 1e-6)
      .text(function(d) { return d; })
    .transition(t)
      .attr("y", 0)
      .style("fill-opacity", 1);
}

i = 0;
// The initial display.
update([base, bases[b]]);
update([g, endings[b][i++]]);	

	


