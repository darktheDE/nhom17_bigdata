# 🛠️ Hướng Dẫn Cài Đặt Môi Trường

## 📋 Yêu Cầu Hệ Thống

### Phần Cứng Tối Thiểu
- **CPU:** 4 cores (khuyến nghị 8 cores)
- **RAM:** 8GB (khuyến nghị 16GB)
- **Ổ cứng:** 50GB trống (khuyến nghị SSD)
- **Mạng:** Kết nối Internet ổn định

### Phần Mềm
- **OS:** CentOS 7/8 hoặc Ubuntu 20.04+
- **Java:** JDK 8 hoặc 11
- **Python:** 3.7+
- **Git:** 2.x

---

## 🔧 Cài Đặt Hadoop Ecosystem

### 1. Cài Đặt Java
```bash
# CentOS
sudo yum install java-11-openjdk java-11-openjdk-devel -y

# Ubuntu
sudo apt update
sudo apt install openjdk-11-jdk -y

# Kiểm tra
java -version
```

### 2. Tạo User Hadoop
```bash
sudo adduser hadoop
sudo usermod -aG wheel hadoop  # CentOS
# hoặc
sudo usermod -aG sudo hadoop   # Ubuntu

# Chuyển sang user hadoop
su - hadoop
```

### 3. Cài Đặt Hadoop
```bash
# Download Hadoop
cd ~
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz

# Giải nén
tar -xzf hadoop-3.3.6.tar.gz
mv hadoop-3.3.6 hadoop

# Cấu hình biến môi trường
echo 'export HADOOP_HOME=/home/hadoop/hadoop' >> ~/.bashrc
echo 'export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop' >> ~/.bashrc
echo 'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> ~/.bashrc
source ~/.bashrc
```

### 4. Cấu Hình Hadoop

#### a) Cấu hình `core-site.xml`
```bash
nano $HADOOP_HOME/etc/hadoop/core-site.xml
```
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

#### b) Cấu hình `hdfs-site.xml`
```bash
nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
```
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/hadoop/hadoop_data/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/hadoop/hadoop_data/hdfs/datanode</value>
    </property>
</configuration>
```

#### c) Tạo thư mục lưu trữ
```bash
mkdir -p ~/hadoop_data/hdfs/namenode
mkdir -p ~/hadoop_data/hdfs/datanode
```

#### d) Format NameNode
```bash
hdfs namenode -format
```

### 5. Khởi Động Hadoop
```bash
# Start HDFS
start-dfs.sh

# Kiểm tra
jps
# Output: NameNode, DataNode, SecondaryNameNode

# Kiểm tra Web UI
# http://localhost:9870
```

---

## 🐝 Cài Đặt Apache Hive

### 1. Download & Cài Đặt
```bash
cd ~
wget https://downloads.apache.org/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz
tar -xzf apache-hive-3.1.3-bin.tar.gz
mv apache-hive-3.1.3-bin hive

# Cấu hình biến môi trường
echo 'export HIVE_HOME=/home/hadoop/hive' >> ~/.bashrc
echo 'export PATH=$PATH:$HIVE_HOME/bin' >> ~/.bashrc
source ~/.bashrc
```

### 2. Cấu Hình Hive
```bash
cd $HIVE_HOME/conf
cp hive-default.xml.template hive-site.xml
nano hive-site.xml
```

### 3. Tạo Thư Mục HDFS cho Hive
```bash
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -mkdir -p /tmp
hdfs dfs -chmod g+w /user/hive/warehouse
hdfs dfs -chmod g+w /tmp
```

### 4. Khởi Động Hive
```bash
# Khởi tạo schema
schematool -initSchema -dbType derby

# Start Hive
hive
```

---

## 🐍 Cài Đặt Python & Dependencies

### 1. Cài Đặt Python 3
```bash
# CentOS
sudo yum install python3 python3-pip -y

# Ubuntu
sudo apt install python3 python3-pip -y
```

### 2. Tạo Virtual Environment
```bash
cd ~/nhom17-bigdata-analytics
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài Đặt Packages
```bash
pip install --upgrade pip
pip install beautifulsoup4 requests pandas numpy selenium
```

---

## 📊 Cài Đặt Power BI (Windows)

1. Download Power BI Desktop từ [Microsoft Store](https://powerbi.microsoft.com/desktop/)
2. Cài đặt và khởi động Power BI Desktop
3. Import dữ liệu từ file CSV trong `data/processed_for_bi/`

---

## 📈 Cài Đặt Grafana (Optional)

### 1. Cài Đặt Grafana
```bash
# CentOS
sudo yum install -y https://dl.grafana.com/oss/release/grafana-10.0.0-1.x86_64.rpm
sudo systemctl start grafana-server
sudo systemctl enable grafana-server

# Ubuntu
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install grafana
sudo systemctl start grafana-server
```

### 2. Truy Cập Grafana
- URL: `http://localhost:3000`
- Default login: `admin/admin`

---

## ✅ Kiểm Tra Cài Đặt

### 1. Kiểm tra HDFS
```bash
hdfs dfs -ls /
```

### 2. Kiểm tra Hive
```bash
hive -e "SHOW DATABASES;"
```

### 3. Kiểm tra Python
```bash
python --version
pip list
```

---

## 🐛 Troubleshooting

### Lỗi: "Connection refused" khi truy cập HDFS
```bash
# Kiểm tra HDFS có chạy không
jps

# Nếu không có NameNode/DataNode, restart
stop-dfs.sh
start-dfs.sh
```

### Lỗi: Hive không kết nối được
```bash
# Xóa metastore cũ và khởi tạo lại
rm -rf metastore_db/
schematool -initSchema -dbType derby
```

### Lỗi: Permission denied trên HDFS
```bash
hdfs dfs -chmod -R 777 /user/hive/warehouse
hdfs dfs -chmod -R 777 /tmp
```

---

## 📚 Tài Liệu Tham Khảo

- [Hadoop Official Documentation](https://hadoop.apache.org/docs/)
- [Hive Official Documentation](https://hive.apache.org/)
- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
