// Firebase 및 필요한 패키지 가져오기
import { initializeApp } from "firebase/app";
import { getStorage, ref, listAll, getDownloadURL } from "firebase/storage";

// Firebase 설정
const firebaseConfig = {
  apiKey: "AIzaSyCuQwqOR30xvh8MM3moR4Bkmqo9klXAv0c",
  authDomain: "final-project-8f802.firebaseapp.com",
  projectId: "final-project-8f802",
  storageBucket: "final-project-8f802.appspot.com",
  messagingSenderId: "285655468516",
  appId: "1:285655468516:web:f15e181a72a386d1219ff1",
  measurementId: "G-4218BPBW39",
};

// Firebase 초기화
const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

// 특정 폴더의 파일 가져오기
const fetchFilesFromFolder = async (folderName) => {
  try {
    const folderRef = ref(storage, folderName); // 폴더 참조
    const res = await listAll(folderRef); // 폴더 내 모든 파일/디렉토리 목록 가져오기

    const urls = await Promise.all(
      res.items.map(async (itemRef) => {
        const downloadURL = await getDownloadURL(itemRef); // 각 파일의 다운로드 URL 가져오기
        return { name: itemRef.name, url: downloadURL };
      })
    );

    console.log(`Files in folder "${folderName}":`, urls);
    return urls; // 파일 이름 및 URL 반환
  } catch (error) {
    console.error(`Error fetching files from folder "${folderName}":`, error);
    throw error;
  }
};

// 모든 폴더의 파일 가져오기
const fetchAllFiles = async () => {
  const folderNames = [
    "1_WordCloud",
    "2_NegativeReview_Ratio",
    "3_Distribution",
    "4_Keyword",
    "5_RadarChart",
  ];

  const allFiles = {};

  for (const folderName of folderNames) {
    allFiles[folderName] = await fetchFilesFromFolder(folderName);
  }

  console.log("All files:", allFiles);
  return allFiles; // 모든 폴더의 파일 정보 반환
};

// 실행
fetchAllFiles()
  .then((files) => console.log("Fetched all files:", files))
  .catch((error) => console.error("Error fetching files:", error));
