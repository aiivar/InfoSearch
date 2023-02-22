package ru.itis.aivarmusa.infosearch;

import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class Downloader {

    public static final String PAGES_DOWNLOADED_COUNT = "pagesDownloadedCount";
    public static final String MAP_WITH_PAGES = "mapWithPages";
    public static final String PROCESSED_LINKS = "processedLinks";

    @Autowired
    private InMemoryCache inMemoryCache;

    @Autowired
    private HtmlFileUtils htmlFileUtils;

    public Optional<Set<String>> download(String url) throws IOException {
        if (url == null || !url.startsWith("http")) {
            return Optional.empty();
        }
        Connection.Response resp = Jsoup.connect(url).userAgent("Mozilla").ignoreHttpErrors(true).timeout(10 * 1000).execute();
        String contentType = resp.contentType();
        if (contentType != null && contentType.contains("text/html")) {
            Integer count = (Integer) inMemoryCache.get(PAGES_DOWNLOADED_COUNT, 0);
            count++;
            String fileName = count + ". " + UUID.randomUUID();
            Document document = resp.parse();
            htmlFileUtils.save(fileName, document.outerHtml());
            inMemoryCache.put(PAGES_DOWNLOADED_COUNT, count);
            Map<String, String> mapWithPages = (Map<String, String>) inMemoryCache.get(MAP_WITH_PAGES, new ConcurrentHashMap<String, String>());
            mapWithPages.put(String.valueOf(count), url);
            inMemoryCache.put(MAP_WITH_PAGES, mapWithPages);
            Set<String> processedLinks = (Set<String>) inMemoryCache.get(PROCESSED_LINKS, new HashSet<String>());
            processedLinks.add(url);
            inMemoryCache.put(PROCESSED_LINKS, processedLinks);
            return Optional.ofNullable(parseLinks(document));
        } else {
            return Optional.empty();
        }
    }

    private Set<String> parseLinks(Document document) {
        Elements links = document.select("a[href]");
        Set<String> linksResult = new HashSet<>();
        for (Element link : links) {
            String attr = link.attr("abs:href");
            if (!attr.isBlank()) {
                linksResult.add(attr);
            }
        }
        return linksResult;
    }

}
