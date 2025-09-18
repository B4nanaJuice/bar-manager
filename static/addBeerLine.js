function addBeerLine(parent, before) {
  beerLine = document.createElement("li");
  beerLine.innerHTML = `
    <input name="beerName" type="text" placeholder="Nom" required />
    <input name="beerType" type="text" placeholder="Type" required />
    <input name="beerDegree" type="number" placeholder="Degré" required />
    <button type="button" onclick="this.parentElement.remove()">X</button>
  `;

  parent.insertBefore(beerLine, before);
}
