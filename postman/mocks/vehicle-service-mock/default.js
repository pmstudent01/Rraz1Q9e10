const http = require("http");

const server = http.createServer((req, res) => {
  const method = req.method;
  const urlObj = new URL(req.url, `http://localhost`);
  const pathname = urlObj.pathname;

  // Match /vehicles/:id pattern
  const vehicleByIdMatch = pathname.match(/^\/vehicles\/([^/]+)$/);

  // @endpoint GET /vehicles
  if (method === "GET" && pathname === "/vehicles") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify([
      {
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159864
      },
      {
        "id": 2,
        "nickName": "Dolly",
        "vin": "JN8AZ2KR1AT169594",
        "make": "Nissan",
        "model": "Cube",
        "year": "2010",
        "miles": 59000
      }
    ]));

  // @endpoint POST /vehicles
  } else if (method === "POST" && pathname === "/vehicles") {
    let body = "";
    req.on("data", chunk => { body += chunk; });
    req.on("end", () => {
      res.writeHead(201, { "Content-Type": "application/json" });
      res.end(JSON.stringify({
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": "159,864"
      }));
    });

  // @endpoint GET /vehicles/:id
  } else if (method === "GET" && vehicleByIdMatch) {
    const id = vehicleByIdMatch[1];
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      "id": parseInt(id) || 1,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": 159864
    }));

  // @endpoint PATCH /vehicles/:id
  } else if (method === "PATCH" && vehicleByIdMatch) {
    let body = "";
    req.on("data", chunk => { body += chunk; });
    req.on("end", () => {
      const id = vehicleByIdMatch[1];
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({
        "id": parseInt(id) || 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159999
      }));
    });

  // @endpoint DELETE /vehicles/:id
  } else if (method === "DELETE" && vehicleByIdMatch) {
    res.writeHead(204, {});
    res.end("");

  } else {
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ "error": "Not Found" }));
  }
});

server.listen(process.env.PORT || 4500);
