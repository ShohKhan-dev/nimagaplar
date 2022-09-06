const chips = document.getElementById('chip-field');
const keyword_in = document.getElementById('keyword-input');

    function makehtml(data){

        if (Array.isArray(data)){
                    chips.innerHTML = ""
                    data.forEach(model=> {
                        chips.innerHTML += `<div class="chip" id="word-${model.id}"> 
                                                ${model.word} 
                                                <span class="closebtn" onClick="removeword(${model.id})">&times;</span>
                                            </div>`
        
                    })
                }

    }


    function ajax_submit()
    {
          
        
        $.ajax({
            type : "POST", 
            url: "{% url 'profile' %}",
            data: {
                keywords : $('#keyword-input').val(),
                csrfmiddlewaretoken: '{{ csrf_token }}'
        
            },
            dataType: "json",
            
            success: function(res){
                keyword_in.value = '';
                
                const data = res.words;

                makehtml(data);
            },
        
            failure: function() {
                
            }
        
        
        });
                  
    };

    function removeword(id) {
            $.ajax({
                url: '{% url "profile" %}',
                data: {
                    'id': id,
                },
                dataType: 'json',
                
                success: function (res) {

                    const data = res.words;

                    makehtml(data);

                    $("#word-" + id).remove();
                    

                }
            });
        };



    window.onload = function() {

        $.ajax({
            url: "{% url 'profile' %}",
            data: {
                'send':'sendata'
            },

            dataType: "json",
            
            success: function(res){
                keyword_in.value = '';
                
                const data = res.words;

                makehtml(data);
            },
        
            failure: function() {
                
            }
        
        
        });
        
    };