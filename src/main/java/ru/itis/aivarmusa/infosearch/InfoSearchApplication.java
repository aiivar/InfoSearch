package ru.itis.aivarmusa.infosearch;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

@SpringBootApplication
public class InfoSearchApplication {

    public static void main(String[] args) {
        ConfigurableApplicationContext applicationContext = SpringApplication.run(InfoSearchApplication.class, args);
        Crawler crawler = applicationContext.getBean(Crawler.class);
        crawler.starInitCrawling();
    }

}
