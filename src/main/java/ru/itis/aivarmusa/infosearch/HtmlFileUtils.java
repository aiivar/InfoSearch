package ru.itis.aivarmusa.infosearch;

import jakarta.annotation.PostConstruct;
import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@Service
public class HtmlFileUtils {

    @Value("${folder.html}")
    private String folderName;

    @PostConstruct
    public void init() {
        try {
            if (!Files.exists(Path.of(folderName))) {
                Files.createDirectory(Path.of(folderName));
            } else {
                FileUtils.deleteDirectory(Path.of(folderName).toFile());
                Files.createDirectory(Path.of(folderName));
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void save(String fileName, String htmlText) {
        try (FileWriter fileWriter = new FileWriter(String.valueOf(Paths.get(folderName, fileName + ".html")))) {
            fileWriter.write(htmlText);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}
