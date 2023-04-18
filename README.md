# CyberPhish Shield - Detecting Phishing URLs
## _Hackathon JunctionXHanoi 2023 - Viettel Academy - MSEC team_

# About our solution
Phishing attacks are a serious threat to individuals and organizations, but they can be combated with a combination of techniques. Rule-based detection can identify known phishing URLs, while URL-based techniques can detect previously unknown URLs. Content-based techniques can analyze website content for potential phishing attacks, and host-based techniques can monitor system behavior. By combining these techniques and utilizing AI and ML, a high rate of detection can be achieved to protect against phishing attacks.
In addition, our approach to building a phishing URL detection system also incorporates microservice architecture and cloud technology to enhance its performance. By leveraging the scalability and flexibility of cloud infrastructure and deploying the system as a set of loosely coupled microservices, we can achieve faster and more efficient processing of data. This allows us to handle large volumes of requests and data, and effectively utilize AI and ML techniques to achieve a high level of accuracy in detecting phishing URLs.
# Technical details
- ✨2 ML Models✨
- ✨Microservice + Kubernetes +  Scale containers✨
- ✨Kafka - Big data✨
- ✨Fast API + GUI Flask python✨
# Final results
- System performance: ~1-2s/URL, >1000 requests/s
- Link web-based application: [Detect Phishing URLs](http://42.96.42.99:3400/)
- Presentation: [Detecting Phishing URLs Presentation](https://drive.google.com/drive/folders/1SQx2JPiDt6ZnVu9dO2mfNar2lg0m6QKB?usp=sharing)
- Real-time Extension-based application to warning phishing URLs for users
# Future development
- Expand the system to other platforms
- Improve the speed of classifying URLs
- Increase the number of requests per seconds 
- Apply some takedown methods to prevent URLs from being widely spreaded

## Features
- Web-based application
    - Import a .json, .csv, .txt file list of URLs to classify URLs into 2 groups: Phishing and Legitimate
    - Enter one URL to see the result
    - Dashboard to see the statistic of the result
    - Take actions with the URL entered: proceed, block or (report, send email - in future)
- Extension-based application
    - Browser extension
    - Give out information of the URL before users proceed to it

Not enough as [MSEC team] [df1]'s expectation but a foundation and motivation for us to continue to develop and maintain applications.

> MSEC team
> </br>
> "Trying our best for a clean CyberSpace"
> </br>
> Spreading not only our knowledge but our enthusiasm for Security field <1

## Installation

## Docker
Test
```sh
cd dillinger
docker build -t <youruser>/dillinger:${package.json.version} .
```
This will create the dillinger image and pull in the necessary dependencies.

```sh
docker run -d -p 8000:8080 --restart=always --cap-add=SYS_ADMIN --name=dillinger <youruser>/dillinger:${package.json.version}
```

> Note: 

```sh
127.0.0.1:8000
```
## About our team
- [Tran Bao Trung](https://github.com/trung501)
- [Chu Tuan Kiet](https://github.com/kimstars)
- [Nguyen Cong Hai Nam](https://github.com/kptis)
- [Khong Phuong Thao](https://github.com/kptis)

> Happy hacking, guys!

