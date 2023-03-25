//필요한 모든 요소 선택
const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button"),
input = dropArea.querySelector("input");
let file; // file 전역 변수.


var send = document.getElementById("submitButton");
send.addEventListener("click", function () {
  console.log("ddd");
  var form = document.getElementById("form");
  var file = document.getElementById('upload-file').files[0];

  form.action = "http://localhost:5000/file_upload";
  form.mothod = "Post";
  form.submit();
});

button.onclick = ()=>{
  input.click(); // 사용자가 버튼을 클릭하면 입력도 클릭.
}

input.addEventListener("change", function(){
  //사용자 선택 파일 가져오기, [0] 이것은 사용자가 여러 파일을 선택하는 경우 첫 번째 파일만 가져옴
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); //함수 호출
});


//사용자가 DropArea 위로 파일을 드래그하는 경우
dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); //기본 동작 방지
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//사용자가 DropArea에서 드래그한 파일을 남겨두는 경우
dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload Image";
});

//사용자가 DropArea에 파일을 드롭하는 경우
dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); //기본 동작 방지
  file = event.dataTransfer.files[0]; //여러파일을 선택하면 첫번째 파일을 가져옴
  showFile(); //calling function

});

function showFile(){
  let fileType = file.type;//선택된 파일 형식 가져오기
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"];//배열에 유효한 이미지를 확장 추가함
  if(validExtensions.includes(fileType)){
    let fileReader = new FileReader(); //사용자가 선택한 파일이 이미지 파일인 경우
    fileReader.onload = ()=>{
      let fileURL = fileReader.result; //fileURL 변수에 사용자 파일 소스 전달
      //let imgTag = `<img src="${fileURL}" alt="">`; //img 태그를 생성하고 src 속성 내부에 사용자가 선택한 파일 소스 전달
      //dropArea.append(imgTag); //dropArea 컨테이너 내부에 생성된 img 태그 추가
      const img = document.createElement('img')
      img.src = fileURL
      dropArea.appendChild(img)

      var con = document.getElementById("front0");
      var con1 = document.getElementById("front1");
      var con2 = document.getElementById("front2");
      var con3 = document.getElementById("front3");
      con.style.display = 'none';
      con1.style.display = 'none';
      con2.style.display = 'none';
      con3.style.display = 'none';
    }
    fileReader.readAsDataURL(file);
  }else{
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}