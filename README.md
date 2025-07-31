
<img width="1892" height="933" alt="5" src="https://github.com/user-attachments/assets/543a936c-f029-4994-aa21-c4c5e5ce42c6" />
<img width="1898" height="776" alt="4" src="https://github.com/user-attachments/assets/e8a40dc8-8ee9-462b-8cab-0236e6587bdf" />
<img width="1881" height="796" alt="3" src="https://github.com/user-attachments/assets/b23681b2-6116-49c3-b07b-a9cecfee89c3" />
<img width="1916" height="707" alt="2" src="https://github.com/user-attachments/assets/739fcd3c-0ff0-4c41-8b64-bfabba817bc5" />
<img width="1657" height="715" alt="Capture" src="https://github.com/user-attachments/assets/d7a0ddfd-86fb-40c4-8dc1-74fd87c9944e" />
<img width="1914" height="964" alt="6" src="https://github.com/user-attachments/assets/4793d5b8-a505-44fb-af6c-9b0e17de4536" />
# 🏥 Tounsvi Medical Store Management System

A complete **Streamlit-based Medical Store Management App** with intelligent stock management, shortage prediction, customer tracking, and invoice generation — developed to simplify and optimize small-scale medical store operations.

---

## 📌 Features

- ✅ **Add New Stock** with expiry, purchase price, supplier, and category tracking  
- 💊 **Sell Medicines** with automatic stock reduction and customer detail recording  
- 📈 **Shortage Prediction** using a trained Random Forest model based on expiry, category, sales, and more  
- 🧾 **Invoice Generation** with medicine details, pricing, and download option  
- 👥 **Customer Tracking** with automatic name recall on repeat visits  
- 📦 **Stock View** with expiry and shortage alerts  
- 🏠 **Home Page Dashboard** for easy navigation and overview  
- 🔐 **Session Management** to preserve data during runtime  

---

## 🤖 Machine Learning Integration

A pre-trained **Random Forest Classifier** predicts stock shortage based on:
- Purchase date and expiry
- Category and supplier
- Units purchased and sold
- Medicine-specific trends

📁 Model file: `medical_stock_data.pkl`  
📊 Trained using data from: `medical_stock_data.csv`

---

## 🚀 How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/medical-store-manager.git
   cd medical-store-manager
