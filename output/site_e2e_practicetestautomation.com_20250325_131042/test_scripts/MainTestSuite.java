import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
    Batch1TestSuite.class, Batch2TestSuite.class
})
public class MainTestSuite {
    // This class will run all batch test suites
}
