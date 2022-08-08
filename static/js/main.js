let search_form = document.getElementById('search_form')
let page_link = document.getElementsByClassName('page-link')

if (search_form){
  for (let i = 0; i < page_link.length; i++){
    page_link[i].addEventListener('click', function (e) {
      e.preventDefault()
      
      let page = this.dataset.page
      
      search_form.innerHTML += `<input value=${page} name="page" hidden/>`    // inja ` estefade shode na ''

      search_form.submit()
    
    })
  }
}