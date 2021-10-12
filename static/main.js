const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')

const confirmBtn = document.getElementById('confirm-btn')
const input = document.getElementById('id_file')
const text = document.getElementById('text')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

input.addEventListener('change', ()=> {
    console.log('changed')

    text.innerHTML = `<p>Select the text portion of the image</p>`
    alertBox.innerHTML = ""
    
    confirmBtn.classList.remove('not-visible')

    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)

    imageBox.innerHTML = `<img src="${url}" id="image">`

    const image = document.getElementById('image')

    const cropper = new Cropper(image, {
        // aspectRatio: 16 / 9,
        crop(event) {
          console.log(event.detail.x);
          console.log(event.detail.y);
          console.log(event.detail.width);
          console.log(event.detail.height);
          console.log(event.detail.rotate);
          console.log(event.detail.scaleX);
          console.log(event.detail.scaleY);
        },
      });

      // cropper.getCroppedCanvas();

      // cropper.getCroppedCanvas({
      //   width: 160,
      //   height: 90,
      //   minWidth: 256,
      //   minHeight: 256,
      //   maxWidth: 4096,
      //   maxHeight: 4096,
      //   fillColor: '#fff',
      //   imageSmoothingEnabled: false,
      //   imageSmoothingQuality: 'high',
      // });

      confirmBtn.addEventListener('click', ()=> {

        cropper.getCroppedCanvas().toBlob((blob)=> {
          const fd = new FormData()
          fd.append('csrfmiddlewaretoken', csrf[0].value)
          fd.append('file', blob, 'my-image.png')

          $.ajax({
            type: 'POST',
            url: imageForm.action,
            enctype: 'multipart/form-data',
            data: fd,

            success: function(response){
              console.log(response)
              
              text.innerHTML = ""
              alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                      ${response.context.filter_predicted_result} was extracted from the image.
                                    </div>`
              // window.location.href = "/text"
              // alert(response.context.filter_predicted_result)
            },
            error: function(error){
              console.log(error)
              alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                      Oops! Something went wrong!
                                    </div>`

              console.log('i got to the error')
            },
            cache: false,
            contentType: false,
            processData: false
          })
        })
      })
})

