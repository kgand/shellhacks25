using UnityEngine;
using UnityEngine.UI; // 引入UI命名空间
using System.Collections;

public class IntroSequenceController : MonoBehaviour
{
    [Header("组件引用")]
    [SerializeField] private NarrationController narrationController;
    [SerializeField] private GameObject continueIcon;
    [SerializeField] private Button inputCatcherButton;
    [SerializeField] private CanvasGroup narrationPanelCanvasGroup; // 用于淡入淡出

    [Header("叙事内容")]
    [TextArea(3, 10)]
    [SerializeField] private string[] sequenceLines; // 在这里填入我们的开场剧本

    private int currentLineIndex = 0;
    private bool waitingForInput = false;

    void Start()
    {
        // 确保UI初始状态正确
        continueIcon.SetActive(false);
        inputCatcherButton.onClick.AddListener(OnScreenClicked); // 监听按钮点击
        
        StartCoroutine(StartSequence());
    }

    private IEnumerator StartSequence()
    {
        // 1. 淡入叙事面板
        yield return FadeCanvasGroup(narrationPanelCanvasGroup, 0f, 1f, 1f);

        // 2. 开始逐行显示
        ShowNextLine();
    }

    private void ShowNextLine()
    {
        if (currentLineIndex < sequenceLines.Length)
        {
            // 隐藏"继续"图标，并开始显示新的一行
            continueIcon.SetActive(false);
            narrationController.DisplayLine(sequenceLines[currentLineIndex]);
            StartCoroutine(WaitForLineFinish());
        }
        else
        {
            // 3. 所有行都显示完毕，结束序列
            StartCoroutine(EndSequence());
        }
    }

    private IEnumerator WaitForLineFinish()
    {
        // 等待NarrationController的打字机效果结束
        yield return new WaitUntil(() => !narrationController.isTyping);

        // 打字结束后，显示"继续"图标，并等待玩家输入
        continueIcon.SetActive(true);
        waitingForInput = true;
    }

    private void OnScreenClicked()
    {
        if (waitingForInput)
        {
            waitingForInput = false;
            currentLineIndex++;
            ShowNextLine();
        }
    }

    private IEnumerator EndSequence()
    {
        // 禁用点击按钮
        inputCatcherButton.gameObject.SetActive(false);
        // 淡出叙事面板
        yield return FadeCanvasGroup(narrationPanelCanvasGroup, 1f, 0f, 1f);
        
        // （可选）在这里可以激活玩家控制器或其他游戏逻辑
        Debug.Log("开场叙事结束！");
        // gameObject.SetActive(false); // 完成后禁用自身
    }

    // 一个通用的CanvasGroup淡入淡出协程
    private IEnumerator FadeCanvasGroup(CanvasGroup cg, float start, float end, float duration)
    {
        float timer = 0f;
        while (timer < duration)
        {
            timer += Time.deltaTime;
            cg.alpha = Mathf.Lerp(start, end, timer / duration);
            yield return null;
        }
        cg.alpha = end;
    }
}