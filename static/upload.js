//필요한 모든 요소 선택
const dropArea = document.querySelector(".drag-area"),
  dragText = dropArea.querySelector("header"),
  button = dropArea.querySelector("button"),
  input = dropArea.querySelector("input");
let file;

var send = document.getElementById("submitButton");
send.addEventListener("click", function () {
  var form = document.getElementById("form");
  var file = document.getElementById("upload-file").files[0];

  if (file) {
    form.action = "/file_upload";
    form.method = "Post";
    form.submit();
  } else {
    console.log("파일이 없어!");
    alert("파일을 넣어주세요");
  }
});

button.onclick = () => {
  input.click(); // 사용자가 버튼을 클릭하면 입력도 클릭.
};

input.addEventListener("change", function () {
  file = this.files[0];
  console.log(file);
  dropArea.classList.add("active");
  showFile();
});

//사용자가 DropArea 위로 파일을 드래그하는 경우
dropArea.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//사용자가 DropArea에서 드래그한 파일을 남겨두는 경우
dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload Image";
});

//사용자가 DropArea에 파일을 드롭하는 경우
dropArea.addEventListener("drop", (event) => {
  event.preventDefault();
  file = event.dataTransfer.files[0];
  $("input[type='file']").prop("file", file);
  showFile();
});

function showFile() {
  let fileType = file.type;
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
  if (validExtensions.includes(fileType)) {
    let fileReader = new FileReader();
    fileReader.onload = () => {
      let fileURL = fileReader.result;
      const img = document.createElement("img");
      img.src = fileURL;
      dropArea.appendChild(img);

      var con = document.getElementById("front0");
      var con1 = document.getElementById("front1");
      var con2 = document.getElementById("front2");
      var con3 = document.getElementById("front3");
      con.style.display = "none";
      con1.style.display = "none";
      con2.style.display = "none";
      con3.style.display = "none";
    };
    fileReader.readAsDataURL(file);
  } else {
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}
