$(document).ready(function() {

    console.log('AI Camp is for the best of the best.')
    
    $('#loading').hide()

    $('#text_gen_button').click(function() {
        console.log('text gen button is clicked');
        var prompt = $('#prompt').val();
        console.log('text gen input value is');
        console.log(prompt);
        var url = 'generate_text'

        $('#loading').show();

        $.post(
            url, 
            {
                'prompt': prompt
            },
            function(data) {
                console.log(data);
                var list_html = "";
                var probability = data['Probability'];
                if (probability <= 0.5) {
                  var statement = "The model detects nonnegative sentiment"
                }
                else {
                  var statement = "The model detects negative sentiment"
                }
                var label = data['Label']
                list_html += "<p id='sentiment_probability'>" + statement + "</p>"
                $("#generated_result").html(list_html);


                $("#loading").hide();
            }

        ).fail(function() {
          alert( "There is something unexpected happened. Email hello@ai-camp.org to report your findings." );
        });

    });

    $()
});