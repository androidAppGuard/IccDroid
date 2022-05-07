package plugins.jacoco;

public interface FinishListener {
    void dumpIntermediateCoverage(String filePath);
}