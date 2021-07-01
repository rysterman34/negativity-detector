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
                var label = data['Label']
                list_html += "<p id='sentiment_probability'> According to the model, there is a " + probability + " chance that the message's sentiment is negative </p>"
                $("#generated_result").html(list_html);


                $("#loading").hide();
            }

        ).fail(function() {
          alert( "There is something unexpected happened. Email hello@ai-camp.org to report your findings." );
        });

    });

    $()
});