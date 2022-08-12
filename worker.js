addEventListener("fetch", event => {
  event.respondWith(handleRequest(event.request))
})

salt = "QueerBot"

async function handleRequest(request) {
    let req = await request
    let myHeaders =await req.headers
    contentType = headers.get('content-type')
    if (contentType = "application/json"){
        try {
            //Parse request as json
            body = await req.json()
            //Get the authentication Hash
            hash = body["hash"];
            //Clone the request json
            contents = { ...body};
            //Delete the hash from it
            delete contents["hash"]
        } catch (err) {
            return new Response(err) //Return the error if one occuirs
        }
    } else {
        return new Response("Only json data, as a POST request is allowed",status=405)
    }

    
    let valid = await validate(contents, hash)
    let res = new Response(valid);
    console.log(valid)
    return res;
}



async function validate(contents, hash){
    let content = ""
    Object.keys(contents) //Get the keys
      .sort()//Sort the keys
      .forEach( //And add each element, by alphabetical order of key, to content string
          key => content += contents[key]
      );
    const password = await QueerBot.get("password")
    const myText = new TextEncoder().encode(content+salt+password);

    const myDigest = await crypto.subtle.digest(
      {
        name: 'SHA-512',
      },
      myText // The data you want to hash as an ArrayBuffer
    );

    let validHash = JSON.stringify(new Uint8Array(myDigest));
    return validHash == hash
}
