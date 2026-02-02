using UnityEngine;
using TMPro;
using UnityEngine.SceneManagement;

public class StoryManager : MonoBehaviour
{
    public static StoryManager Instance { get; private set; }

    [Header("游戏状态")]
    public int memoryClarityScore = 0;

    // UI 引用现在由外部脚本主动注册
    private TextMeshProUGUI scoreText;
    public NarrationController narrationController { get; private set; } // 允许外部读取，但只能内部设置

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    
    // 我们不再需要 OnEnable/OnDisable 和 OnSceneLoaded 了
    // 因为UI元素会自我注册

    // --- 新的注册方法 ---
    public void RegisterNarrationController(NarrationController controller)
    {
        narrationController = controller;
        Debug.Log("NarrationController has been registered with the StoryManager.");
    }
    
    public void RegisterScoreText(TextMeshProUGUI textUI)
    {
        scoreText = textUI;
        UpdateScoreUI(); // 注册后立即更新一次
        Debug.Log("ScoreText has been registered with the StoryManager.");
    }
    // --- 注册方法结束 ---

    public void ChangeClarity(int amount)
    {
        memoryClarityScore += amount;
        UpdateScoreUI();
    }

    void UpdateScoreUI()
    {
        if (scoreText != null)
        {
            scoreText.text = "记忆清晰度: " + memoryClarityScore;
        }
    }
    
    public void ShowNarration(string narrationText)
    {
        if (narrationController != null)
        {
            narrationController.DisplayLine(narrationText);
        }
        else
        {
            Debug.LogError("StoryManager: NarrationController has not been registered! Cannot show narration.");
        }
    }
}