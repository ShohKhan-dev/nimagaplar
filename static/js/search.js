

const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultsBox = document.getElementById('results-box')


const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (game) => {
    $.ajax({
        type: 'POST',
        url: '/search/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'game': game,
        },
        success: (res)=> {
            const data = res.data

            if (Array.isArray(data)){
                resultsBox.innerHTML = ""
                data.forEach(model=> {
                    resultsBox.innerHTML += `<a href="/${'model'}/${model.pk}">
                                                <div class="row mt-2 mb-2">
                                                

                                                    <div class="col-2">
                                                        <img src="${model.logo}" alt="model logo" class="model-logo">
                                                    </div>

                                                    <div class="col-10">
													<h5>${model.title}</h5>
                                                        
                                                    </div>
                                                </div>
                                            </a>`
                })
            }
            else{
                if (searchInput.value.length > 0){
                    resultsBox.innerHTML = `<p>${data}</p>`
                }
                else{
                    resultsBox.classList.add('not-visible')
                }
            }
        },
        error: (err)=> {
            console.log(err)
        }
    })
}

searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value)

    if (resultsBox.classList.contains('not-visible')){
        resultsBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value)
})