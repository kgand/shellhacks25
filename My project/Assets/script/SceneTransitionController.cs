using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using System.Collections;

public class SceneTransitionController : MonoBehaviour
{
    public static SceneTransitionController Instance { get; private set; }

    private Image fadeImage; // 改为私有，让它自动寻找
    public float fadeSpeed = 1.5f;

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
    
    // 订阅和取消订阅场景加载事件
    void OnEnable() { SceneManager.sceneLoaded += OnSceneLoaded; }
    void OnDisable() { SceneManager.sceneLoaded -= OnSceneLoaded; }

    // 每次新场景加载完成时，自动调用此方法
    void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
        // 在新场景中，通过名字找到FadeImage
        GameObject fadeImageObject = GameObject.Find("FadeImage");
        if (fadeImageObject != null)
        {
            fadeImage = fadeImageObject.GetComponent<Image>();
            // 开始从黑屏淡入新场景
            StartCoroutine(FadeIn());
        }
        else
        {
            Debug.LogWarning("SceneTransitionController: 在新场景中找不到名为 'FadeImage' 的UI对象！");
        }
    }

    public void FadeToScene(string sceneName)
    {
        StartCoroutine(FadeOut(sceneName));
    }

    private IEnumerator FadeOut(string sceneName)
    {
        if (fadeImage == null) yield break; // 如果没有找到Image，就什么也不做

        float alpha = 0;
        fadeImage.color = new Color(0, 0, 0, alpha);
        fadeImage.raycastTarget = true;

        while (alpha < 1)
        {
            alpha += Time.deltaTime / fadeSpeed;
            fadeImage.color = new Color(0, 0, 0, alpha);
            yield return null;
        }

        SceneManager.LoadScene(sceneName);
    }

    private IEnumerator FadeIn()
    {
        if (fadeImage == null) yield break;

        float alpha = 1;
        fadeImage.raycastTarget = true;

        while (alpha > 0)
        {
            alpha -= Time.deltaTime / fadeSpeed;
            fadeImage.color = new Color(0, 0, 0, alpha);
            yield return null;
        }
        fadeImage.raycastTarget = false;
    }
}