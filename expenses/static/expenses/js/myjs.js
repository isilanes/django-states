function mytoggle(id) {
    const id_queries = document.getElementsByClassName(id);
    for (i = 0; i < id_queries.length; i++) {
        if (id_queries[i].style.display == "none") {
            id_queries[i].style.display = "";
        } else {
            id_queries[i].style.display = "none";
        }
    };
}
