window.onload = function () {
    console.log("Pagina Coșului Virtual încărcată!");
    incarcaCos(); //la refresh, se incarca continutul cosului
    function incarcaCos() {
        const id_uri_cos=localStorage.getItem("cos_virtual"); //extrag cosul din local storage
        const cos_virtual=id_uri_cos ? JSON.parse(id_uri_cos) : {}; //daca exista, il transformam in obiect ca sa lucram cu el
        const tabelBody=document.querySelector("#tabel_cos_virtual tbody"); //selectam tbody-ul tabelului
        tabelBody.innerHTML = ""; 
        console.log(zboruri);
        let totalPret=0;
        let totalObiecte=0;

        for (let id_zbor in cos_virtual) {
            const cantitate=cos_virtual[id_zbor]; //cantitatea de produse din cos
            const zbor=zboruri.find(zbor=>zbor.id===parseInt(id_zbor)); //cautam zborul in lista de zboruri pe baza id-ului

            if (!zbor) {
                console.warn(`Zborul cu ID ${id_zbor} nu a fost găsit.`); //daca nu gasim zborul, afisam un mesaj de avertizare
                continue;
            }

            //creez un rand cu datele zborului
            const rand=document.createElement("tr");
            rand.dataset.id=id_zbor;
            rand.dataset.plecare=zbor.plecare;
            rand.dataset.destinatie=zbor.destinatie;
            rand.dataset.pret=zbor.pret;
            rand.dataset.cantitate=cantitate;
            rand.dataset.pret_total=zbor.pret*cantitate;

            rand.innerHTML = `
                <td>${zbor.plecare}</td>
                <td>${zbor.destinatie}</td>
                <td>${zbor.pret}</td>
                <td>${cantitate}</td>
                <td>${zbor.pret * cantitate}</td>
            `;

            tabelBody.appendChild(rand); //adaugam randul in tabel

            //actualizam totalurile
            totalPret+=zbor.pret*cantitate;
            totalObiecte+=cantitate;
        }

        //actualizam ce se afiseaza
        document.getElementById("pret_total").textContent=totalPret;
        document.getElementById("numar_total_obiecte").textContent=totalObiecte;
    }

        //golim cosul
    document.getElementById("btn_goleste_cos").onclick=function(){
        localStorage.removeItem("cos_virtual");
        incarcaCos();
        console.log("Cosul a fost golit!");
    };

    //ordoneaza cosului dupa un criteriu
    window.ordoneazaCos=function (criteriu) {
        const randuri=Array.from(document.querySelectorAll("#tabel_cos_virtual tbody tr"));
        randuri.sort((a,b)=>{
            if (criteriu==="pret" || criteriu==="pret_total") {
                return parseFloat(a.dataset[criteriu])-parseFloat(b.dataset[criteriu]);
            } else if (criteriu==="cantitate") {
                return parseInt(a.dataset[criteriu])-parseInt(b.dataset[criteriu]);
            } else {
                return a.dataset[criteriu].localeCompare(b.dataset[criteriu]);
            }
        });
        const tabelBody=document.querySelector("#tabel_cos_virtual tbody");
        tabelBody.innerHTML="";
        randuri.forEach(rand => tabelBody.appendChild(rand));
    };
};
