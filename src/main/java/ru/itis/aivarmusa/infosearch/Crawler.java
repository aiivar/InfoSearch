package ru.itis.aivarmusa.infosearch;

import jakarta.annotation.PostConstruct;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

@Service
@Log4j2
public class Crawler {

    public static final String LINKS_TO_PROCESS = "linksToProcess";
    public static final String MAX_PAGES_COUNT = "maxPagesCount";
    public static final int MAX_POSSIBLE_HARDCODED = 110;
    @Value("${downloader.from.url}")
    private String baseUrl;

    @Autowired
    private InMemoryCache inMemoryCache;

    @PostConstruct
    public void init() {
        Set<String> linksToProcess = (Set<String>) inMemoryCache.get(LINKS_TO_PROCESS, new HashSet<String>());
        linksToProcess.add(baseUrl);
        inMemoryCache.put(LINKS_TO_PROCESS, linksToProcess);
        inMemoryCache.put(MAX_PAGES_COUNT, MAX_POSSIBLE_HARDCODED);
    }

    @Autowired
    private Downloader downloader;

    public void starInitCrawling() {
        try {
            log.info("START CRAWLING");
            Set<String> linksToProcess = (Set<String>) inMemoryCache.get(LINKS_TO_PROCESS, new HashSet<String>());
            Optional<Set<String>> downloadedLinks = downloader.download(baseUrl);
            linksToProcess.remove(baseUrl);
            downloadedLinks.filter(links -> !links.isEmpty())
                    .ifPresentOrElse(linksToProcess::addAll, () -> log.warn("No links found: " + baseUrl));
            inMemoryCache.put(LINKS_TO_PROCESS, linksToProcess);
            Integer maxPagesCount = (Integer) inMemoryCache.get(MAX_PAGES_COUNT, MAX_POSSIBLE_HARDCODED);
            Integer processedPages = getProcessedPages();
            while (!linksToProcess.isEmpty() && processedPages < maxPagesCount) {
                Set<String> temp = new HashSet<>();
                Set<String> toRemove = new HashSet<>();
                for (String linkToProcess : linksToProcess) {
                    if (getProcessedPages() >= MAX_POSSIBLE_HARDCODED) {
                        break;
                    }
                    downloadedLinks = downloader.download(linkToProcess);
                    downloadedLinks.filter(links -> !links.isEmpty())
                            .ifPresentOrElse(links -> {
                                Set<String> processedLinks = (Set<String>) inMemoryCache.get(Downloader.PROCESSED_LINKS);
                                for (String link : links) {
                                    if (!processedLinks.contains(link)) {
                                        temp.add(link);
                                    }
                                }
                            }, () -> log.warn("No links found: " + linkToProcess));
                    toRemove.add(linkToProcess);
                }
                linksToProcess.removeAll(toRemove);
                linksToProcess.addAll(temp);
                inMemoryCache.put(LINKS_TO_PROCESS, linksToProcess);
                processedPages = getProcessedPages();
                log.info("PROCESSED PAGES COUNT: " + processedPages);
            }
            saveIndexFile();
            log.info("STOP CRAWLING");
        } catch (IOException e) {
            log.error(e);
        }
    }

    private void saveIndexFile() {
        Map<String, String> map = (Map<String, String>) inMemoryCache.get(Downloader.MAP_WITH_PAGES);
        StringBuilder stringBuilder = new StringBuilder();
        Set<Map.Entry<String, String>> entries = map.entrySet();
        entries.stream().sorted(Comparator.comparingInt(entry -> Integer.parseInt(entry.getKey()))).forEach(entry ->
                stringBuilder.append(entry.getKey()).append(" ").append(entry.getValue()).append("\n")
        );
        try {
            Files.deleteIfExists(Path.of("index.txt"));
            FileWriter fileWriter = new FileWriter("index.txt");
            fileWriter.write(stringBuilder.toString());
            fileWriter.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private Integer getProcessedPages() {
        return (Integer) inMemoryCache.get(Downloader.PAGES_DOWNLOADED_COUNT, MAX_POSSIBLE_HARDCODED);
    }
}
