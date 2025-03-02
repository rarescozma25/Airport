window.onload = function () {
    console.log("fisierul a fost incarcat!");
    var butoane=document.getElementsByClassName("btn_cos_virtual"); //butoanele de adaugat in cos
    for (let btn of butoane) {
        btn.onclick=function () {
            console.log(this);
            let id_uri_cos=localStorage.getItem("cos_virtual");
            console.log("continutul din localStorage inainte de modificare:", id_uri_cos);
            let cos_virtual=id_uri_cos ? JSON.parse(id_uri_cos) : {}; //daca exista id-uri in cos_virtual, le preluam, altfel initializam cu un obiect gol
            let id_produs = this.dataset["id"];
            let capacitate_avion=parseInt(this.dataset["capacitate"],10) || Infinity; //conversie in int(baza 10)
            //limita vreau sa fie data de capacitatea avionului asociat zborului
            console.log(capacitate_avion);

            //daca produsul nu exista in cos_virtual, il adaugam cu cantitatea 0
            if (!cos_virtual[id_produs]) {
                cos_virtual[id_produs]=0;
            }
            //adaugare produs in cos
            if (cos_virtual[id_produs]<capacitate_avion) {
                cos_virtual[id_produs]+=1; //incrementam cantitatea
                console.log(`Produsul ${id_produs} adaugat. Cantitate: ${cos_virtual[id_produs]}`);

                localStorage.setItem("cos_virtual", JSON.stringify(cos_virtual));//actualizam cosul in local storage
                
                actualizeazaTotalCantitate();//pentru tabelul de cantitati de pe pagina
            } else {
                alert("nu poti adauga mai multe produse decat exista în stoc!");
            }

            let articole=document.getElementsByClassName("produs"); //cand apasam pe butonul de adaugare in cos, culoarea se schimba in rosu
            for (let articol of articole) {
                if (cos_virtual[articol.dataset["id"]]) {
                    articol.style.color = "red";
                } else {
                    articol.style.color = "";
                }
            }
            console.log("Continutul din cos dupa modificare:", JSON.stringify(cos_virtual)); //pentru debug
        };
    }
var butoaneConfirmare = document.getElementsByClassName("btn_confirm");
for (let buton of butoaneConfirmare) {
    buton.onclick = function () {
        let id_produs=this.dataset["id"];
        let campInput=document.querySelector(`.cantitate_bilete[data-id="${id_produs}"]`);
        let valoareIntrodusa=parseInt(campInput.value, 10) || 0;
        let capacitate_avion=parseInt(campInput.max, 10) || Infinity;

        if (valoareIntrodusa>capacitate_avion) {
            alert("Nu poți adăuga mai multe bilete decât capacitatea avionului!");
            campInput.value = capacitate_avion;
            valoareIntrodusa = capacitate_avion;
        }

        let id_uri_cos=localStorage.getItem("cos_virtual");
        let cos_virtual=id_uri_cos ? JSON.parse(id_uri_cos) : {};

        if (valoareIntrodusa===0) {
            delete cos_virtual[id_produs];
        } else {
            cos_virtual[id_produs]=valoareIntrodusa;
        }

        localStorage.setItem("cos_virtual", JSON.stringify(cos_virtual));

        actualizeazaTotalCantitate();
        let articole=document.getElementsByClassName("produs");
        for (let articol of articole) {
            if (cos_virtual[articol.dataset["id"]]){
                articol.style.color="red";
            } else {
                articol.style.color="";
            }
        }

        console.log(`Cantitatea pentru produsul ${id_produs} a fost actualizată la ${valoareIntrodusa}.`);
    };
}



    //butoane de scadere
    var butoaneScadere=document.getElementsByClassName("btn_scade");
    for (let btn of butoaneScadere) {
        btn.onclick = function () {
            let id_uri_cos=localStorage.getItem("cos_virtual");
            let cos_virtual=id_uri_cos ? JSON.parse(id_uri_cos):{};
            let id_produs=this.dataset["id"];

            if (cos_virtual[id_produs]) {
                cos_virtual[id_produs]-=1;
                if (cos_virtual[id_produs] <= 0) {
                    delete cos_virtual[id_produs]; // eliminam produsul daca cantitatea e 0
                }
                console.log(`Produsul ${id_produs} scăzut. Cantitate: ${cos_virtual[id_produs] || 0}`);

                //actualizam cosul in local storage
                localStorage.setItem("cos_virtual", JSON.stringify(cos_virtual));

                //recalculam totalul cantitatilor
                actualizeazaTotalCantitate();
            } else {
                alert("produsul nu este în cos.");
            }

            //recoloram produsele
            let articole = document.getElementsByClassName("produs");
            for (let articol of articole) {
                if (cos_virtual[articol.dataset["id"]]){
                    articol.style.color="red";
                } else {
                    articol.style.color="";
                }
            }
        };
    }

    //butonul de golire a cosului
    let butonGolire=document.getElementById("btn_sterge_cos_virtual");
    if (butonGolire){
        butonGolire.onclick=function () {
            localStorage.removeItem("cos_virtual");
            let articole=document.getElementsByClassName("produs");
            for (let articol of articole) {
                articol.style.color=""; //resetam culoarea
            }
            actualizeazaTotalCantitate();

            console.log("Cosul a fost golit.");
        };
    }

    //actualizarea cantitatii totale
    function actualizeazaTotalCantitate() {
        let id_uri_cos=localStorage.getItem("cos_virtual");
        let cos_virtual=id_uri_cos ? JSON.parse(id_uri_cos) : {};

        let totalCantitate=0;

        //adunam toate cantitatile
        for (let id_produs in cos_virtual) {
            totalCantitate+=cos_virtual[id_produs];
        }

        //afisam totalul in tabelul de pe pagina
        let totalElement=document.getElementById("total_bilete");
        if (totalElement){
            totalElement.textContent=totalCantitate;
        }
    }
    actualizeazaTotalCantitate();
};
